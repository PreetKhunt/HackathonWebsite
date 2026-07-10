-- Enhanced database schema for Jharkhand Tourism Website

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enhanced guide bookings table
CREATE TABLE IF NOT EXISTS guide_bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    places TEXT NOT NULL,
    date DATE NOT NULL,
    duration INTEGER NOT NULL,
    group_size INTEGER NOT NULL,
    special_requirements TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_id VARCHAR(255),
    amount DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enhanced transport bookings table
CREATE TABLE IF NOT EXISTS transport_bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    pickup_location VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    passengers INTEGER NOT NULL,
    vehicle_type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_id VARCHAR(255),
    amount DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enhanced activity bookings table
CREATE TABLE IF NOT EXISTS activity_bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    activity VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    participants INTEGER NOT NULL,
    experience_level VARCHAR(50),
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_id VARCHAR(255),
    amount DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Places table (enhanced)
CREATE TABLE IF NOT EXISTS places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    location VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    image_url VARCHAR(500),
    rating DECIMAL(3,2) DEFAULT 0,
    entry_fee DECIMAL(8,2) DEFAULT 0,
    best_time_to_visit VARCHAR(255),
    facilities TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Payment transactions table
CREATE TABLE IF NOT EXISTS payment_transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    booking_type VARCHAR(50) NOT NULL,
    booking_id INTEGER NOT NULL,
    payment_gateway VARCHAR(50) NOT NULL,
    transaction_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    status VARCHAR(50) DEFAULT 'pending',
    gateway_response JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    place_id INTEGER REFERENCES places(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat logs table for AI chatbot analytics
CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question TEXT NOT NULL,
    response TEXT NOT NULL,
    language VARCHAR(50) DEFAULT 'English',
    response_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample places data
INSERT INTO places (name, description, category, location, latitude, longitude, image_url, entry_fee, best_time_to_visit, facilities) VALUES
('Dassam Falls', 'A spectacular cascade on the Kanchi River surrounded by sal forests.', 'Waterfall', 'Bundu, Ranchi', 23.3441, 85.4419, 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/19/fa/bd/6e/a-full-view-of-the-falls.jpg?w=900&h=500&s=1', 10.00, 'October to March', ARRAY['Parking', 'Food Stalls', 'Photography']),
('Hundru Falls', 'Monsoon-favorite plunge pool and scenic rock formations.', 'Waterfall', 'Ranchi', 23.4241, 85.5893, 'https://thumbs.dreamstime.com/b/hundru-waterfalls-jharkhand-287522583.jpg', 15.00, 'July to February', ARRAY['Parking', 'Trekking', 'Swimming']),
('Betla National Park', 'Forests, elephants, and the ruins of Palamu Fort—Jharkhand classic safari.', 'Wildlife', 'Latehar', 23.8833, 84.1833, 'https://superbcollections.com/wp-content/uploads/2023/08/Betla-National-Park.jpeg', 50.00, 'November to June', ARRAY['Safari', 'Accommodation', 'Guide Service']),
('Netarhat', 'Queen of Chotanagpur—famed for sunrise/sunset points and pine avenues.', 'Hill Station', 'Latehar', 23.4667, 84.2667, 'https://thumbs.dreamstime.com/b/netarhat-jharkhand-indian-view-pictures-taken-vishal-singh-170710563.jpg', 0.00, 'October to March', ARRAY['Accommodation', 'Trekking', 'Sunrise Point']),
('Patratu Valley', 'Winding roads, emerald hills, and the shimmering Patratu Lake.', 'Scenic Drive', 'Ramgarh', 23.6800, 85.2800, 'https://media-cdn.tripadvisor.com/media/photo-s/0e/5e/c0/46/drone-shot-of-the-valley.jpg', 0.00, 'October to April', ARRAY['Boating', 'Photography', 'Viewpoint']),
('Baidyanath Temple (Deoghar)', 'One of the 12 Jyotirlingas—vibrant religious hub with old-world charm.', 'Pilgrimage', 'Deoghar', 24.4800, 86.7000, 'https://cdn1.prayagsamagam.com/media/2023/01/25183337/Baidyanath-Dham-1-1024x576.webp', 0.00, 'Year Round', ARRAY['Parking', 'Prasad', 'Accommodation', 'Medical Facility']),
('Parasnath Hill (Shikharji)', 'Important Jain pilgrimage; rewarding hikes and misty viewpoints.', 'Trek', 'Giridih', 23.9200, 86.1500, 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/09/6c/f6/c8/parasnath-hills.jpg?w=1200&h=-1&s=1', 20.00, 'October to March', ARRAY['Trekking', 'Temple', 'Accommodation', 'Guide Service']),
('Ranchi Lake & Rock Garden', 'Relaxing lakeside vibes and sculpted gardens within the city.', 'City', 'Ranchi', 23.3441, 85.3096, 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/18/3d/c0/dd/rock-garden.jpg?w=900&h=500&s=1', 0.00, 'Year Round', ARRAY['Parking', 'Boating', 'Photography']),
('Tribal Handicrafts', 'Local artisans, dokra metal craft, bamboo works—shop responsibly.', 'Marketplace', 'Various Locations', 23.3500, 85.3000, 'https://zineart.in/images/DOK/DOK006011.webp', 0.00, 'Year Round', ARRAY['Shopping', 'Cultural Experience', 'Workshops']);


-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_guide_bookings_user_id ON guide_bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_guide_bookings_date ON guide_bookings(date);
CREATE INDEX IF NOT EXISTS idx_transport_bookings_user_id ON transport_bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_bookings_user_id ON activity_bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_places_category ON places(category);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_user_id ON payment_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_place_id ON reviews(place_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_guide_bookings_updated_at BEFORE UPDATE ON guide_bookings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_transport_bookings_updated_at BEFORE UPDATE ON transport_bookings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_activity_bookings_updated_at BEFORE UPDATE ON activity_bookings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_places_updated_at BEFORE UPDATE ON places FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_payment_transactions_updated_at BEFORE UPDATE ON payment_transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();