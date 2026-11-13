import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import app


class RazorpayPaymentTests(unittest.TestCase):
    def setUp(self):
        self.user = SimpleNamespace(id='user-1', email='traveler@example.com')
        self.gateway = SimpleNamespace(
            order=Mock(),
            payment=Mock(),
            utility=Mock(),
        )
        self.gateway.order.create.return_value = {
            'id': 'order-1',
            'amount': 699900,
            'currency': 'INR',
        }
        self.gateway.order.fetch.return_value = {
            'amount': 699900,
            'currency': 'INR',
            'notes': {'user_id': 'user-1', 'package_name': 'Budget'},
        }
        self.gateway.payment.fetch.return_value = {
            'order_id': 'order-1',
            'amount': 699900,
            'currency': 'INR',
            'status': 'captured',
        }
        self.database = Mock()
        self.database.table.return_value.insert.return_value.execute.return_value = (
            SimpleNamespace(data=[{'id': 'booking-1'}])
        )

        self.patches = [
            patch.object(app, 'get_current_user', return_value=self.user),
            patch.object(app, 'get_razorpay_client', return_value=self.gateway),
            patch.object(app, 'supabase_admin', self.database),
        ]
        for mocked in self.patches:
            mocked.start()
            self.addCleanup(mocked.stop)

        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

    def booking_payload(self):
        return {
            'name': 'Traveler',
            'email': 'traveler@example.com',
            'phone': '9999999999',
            'date': '2026-12-01',
            'package_name': 'Budget',
            'razorpay_order_id': 'order-1',
            'razorpay_payment_id': 'payment-1',
            'razorpay_signature': 'valid-signature',
            'amount': 1,
            'payment_status': 'untrusted',
        }

    def test_order_amount_is_set_by_server_package_price(self):
        response = self.client.post(
            '/api/create-razorpay-order',
            json={'package_name': 'Budget', 'amount': 1},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['amount'], 699900)
        self.gateway.order.create.assert_called_once()
        order_data = self.gateway.order.create.call_args.kwargs['data']
        self.assertEqual(order_data['amount'], 699900)
        self.assertEqual(order_data['notes']['user_id'], 'user-1')

    def test_booking_verifies_payment_and_captures_authorized_payment(self):
        self.gateway.payment.fetch.return_value['status'] = 'authorized'
        self.gateway.payment.capture.return_value = {
            'order_id': 'order-1',
            'amount': 699900,
            'currency': 'INR',
            'status': 'captured',
        }

        response = self.client.post('/api/book-package', json=self.booking_payload())

        self.assertEqual(response.status_code, 200)
        self.gateway.utility.verify_payment_signature.assert_called_once()
        self.gateway.payment.capture.assert_called_once_with('payment-1', 699900)
        saved_booking = self.database.table.return_value.insert.call_args.args[0]
        self.assertEqual(saved_booking['amount'], 6999)
        self.assertEqual(saved_booking['payment_status'], 'paid')

    def test_invalid_signature_never_saves_booking(self):
        self.gateway.utility.verify_payment_signature.side_effect = (
            app.razorpay.errors.SignatureVerificationError('invalid signature')
        )

        response = self.client.post('/api/book-package', json=self.booking_payload())

        self.assertEqual(response.status_code, 400)
        self.database.table.assert_not_called()

    def test_order_amount_mismatch_never_saves_booking(self):
        self.gateway.order.fetch.return_value['amount'] = 1

        response = self.client.post('/api/book-package', json=self.booking_payload())

        self.assertEqual(response.status_code, 400)
        self.database.table.assert_not_called()


if __name__ == '__main__':
    unittest.main()
