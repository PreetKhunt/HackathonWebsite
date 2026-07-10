# -*- coding: utf-8 -*-
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

book_guide_old = """function bookGuide(){
      const data = {
        name: gName.value.trim(),
        phone: gPhone.value.trim(),
        email: gEmail.value.trim(),
        lang: gLang.value,
        place: Array.from(gPlace.selectedOptions).map(o=>o.value),
        date: gDate.value
      };
      if(!data.name || !data.phone || !data.date){ gMsg.textContent = "Please fill name, phone and date."; gMsg.style.color = "#ffaaaa"; return; }
      fetch('/api/book-guide', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      }).then(r => r.json()).catch(e => console.error(e));
      gMsg.textContent = "Guide request submitted! We'll confirm availability shortly.";
      gMsg.style.color = "#9fe29f";
      // simple itinerary kick
      document.getElementById('plan').textContent =
        `Suggested day plan for ${data.place.slice(0,3).join(", ")}:\n• Morning: Meet guide, quick briefing.\n• Mid-day: Site visits & lunch at local eatery.\n• Evening: Sunset view & return.\n• Tips: Carry water, avoid litter, respect local customs.`;
    }"""

book_guide_new = """function bookGuide(){
      const gName = document.getElementById("gName");
      const gPhone = document.getElementById("gPhone");
      const gEmail = document.getElementById("gEmail");
      const gLang = document.getElementById("gLang");
      const gPlace = document.getElementById("gPlace");
      const gDate = document.getElementById("gDate");
      const gMsg = document.getElementById("gMsg");
      const plan = document.getElementById("plan");

      const data = {
        name: gName ? gName.value.trim() : '',
        phone: gPhone ? gPhone.value.trim() : '',
        email: gEmail ? gEmail.value.trim() : '',
        lang: gLang ? gLang.value : '',
        place: gPlace ? Array.from(gPlace.selectedOptions).map(o=>o.value) : [],
        date: gDate ? gDate.value : ''
      };
      if(!data.name || !data.phone || !data.date){ 
          if(gMsg) { gMsg.textContent = "Please fill name, phone and date."; gMsg.style.color = "#ffaaaa"; }
          return; 
      }
      fetch('/api/book-guide', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      }).then(r => r.json()).catch(e => console.error(e));
      
      if(gMsg) {
          gMsg.textContent = "Guide request submitted! We'll confirm availability shortly.";
          gMsg.style.color = "#9fe29f";
      }
      // simple itinerary kick
      if(plan) {
          plan.textContent =
            `Suggested day plan for ${data.place.slice(0,3).join(", ")}:\n• Morning: Meet guide, quick briefing.\n• Mid-day: Site visits & lunch at local eatery.\n• Evening: Sunset view & return.\n• Tips: Carry water, avoid litter, respect local customs.`;
      }
    }"""

book_transport_old = """function bookTransport(){
      const data = {
        name: tName.value.trim(),
        from: tFrom.value.trim(),
        to: tTo.value.trim(),
        vehicle: tVehicle.value,
        when: tDate.value
      };
      if(!data.name || !data.from || !data.to || !data.when){ tMsg.textContent="Please complete all fields."; tMsg.style.color="#ffaaaa"; return; }
      fetch('/api/book-transport', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      }).then(r => r.json()).catch(e => console.error(e));
      tMsg.textContent = "Transport request received! You'll get driver details after assignment.";
      tMsg.style.color = "#9fe29f";
    }"""

book_transport_new = """function bookTransport(){
      const tName = document.getElementById("tName");
      const tFrom = document.getElementById("tFrom");
      const tTo = document.getElementById("tTo");
      const tVehicle = document.getElementById("tVehicle");
      const tDate = document.getElementById("tDate");
      const tMsg = document.getElementById("tMsg");

      const data = {
        name: tName ? tName.value.trim() : '',
        from: tFrom ? tFrom.value.trim() : '',
        to: tTo ? tTo.value.trim() : '',
        vehicle: tVehicle ? tVehicle.value : '',
        when: tDate ? tDate.value : ''
      };
      if(!data.name || !data.from || !data.to || !data.when){ 
          if(tMsg) { tMsg.textContent="Please complete all fields."; tMsg.style.color="#ffaaaa"; }
          return; 
      }
      fetch('/api/book-transport', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      }).then(r => r.json()).catch(e => console.error(e));
      
      if(tMsg) {
          tMsg.textContent = "Transport request received! You'll get driver details after assignment.";
          tMsg.style.color = "#9fe29f";
      }
    }"""

make_plan_old = """function makePlan(){
      const d = parseInt(days.value,10);
      const pace = paceSelectValue();
      const blocks = {
        Relaxed: ["Slow breakfast","One major site","Local lunch","Siesta","Sunset viewpoint","Market stroll"],
        Balanced: ["Early start","2–3 sites","Lunch en-route","Short hike","Café break","Sunset point"],
        Packed: ["Pre-dawn drive","3–4 sites","Pack-lunch","Long hike","Cultural stop","Late drive back"]
      };
      const daily = blocks[pace];
      const skeleton = [
        "Ranchi city + Dassam/Hundru",
        "Patratu Valley drive + Lake",
        "Netarhat day trip",
        "Betla safari + Palamu Fort",
        "Deoghar or Parasnath (as per interest)"
      ];
      let out = [];
      for(let i=0;i<d;i++){
        out.push(`Day ${i+1}: ${skeleton[i] || "Leisure / shopping / buffer"}\n  • ${daily.join("\\n  • ")}`);
      }
      plan.textContent = out.join("\\n\\n");
    }"""

make_plan_new = """function makePlan(){
      const days = document.getElementById("days");
      const plan = document.getElementById("plan");
      const d = parseInt(days ? days.value : "1",10);
      const pace = paceSelectValue();
      const blocks = {
        Relaxed: ["Slow breakfast","One major site","Local lunch","Siesta","Sunset viewpoint","Market stroll"],
        Balanced: ["Early start","2–3 sites","Lunch en-route","Short hike","Café break","Sunset point"],
        Packed: ["Pre-dawn drive","3–4 sites","Pack-lunch","Long hike","Cultural stop","Late drive back"]
      };
      const daily = blocks[pace];
      const skeleton = [
        "Ranchi city + Dassam/Hundru",
        "Patratu Valley drive + Lake",
        "Netarhat day trip",
        "Betla safari + Palamu Fort",
        "Deoghar or Parasnath (as per interest)"
      ];
      let out = [];
      for(let i=0;i<d;i++){
        out.push(`Day ${i+1}: ${skeleton[i] || "Leisure / shopping / buffer"}\\n  • ${daily.join("\\n  • ")}`);
      }
      if(plan) plan.textContent = out.join("\\n\\n");
    }"""

map_old = """    // --------- Map (Leaflet + OSM) ----------
    document.addEventListener("DOMContentLoaded", function () {
      // Initialize map
      var map = L.map('map').setView([23.6102, 85.2799], 7);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);

      // Add markers with clickable links to Google Maps
      const sites = [
        { name: "Hundru Falls", coords: [23.6355, 85.3096] },
        { name: "Jonha Falls", coords: [23.3700, 85.3300] },
        { name: "Dassam Falls", coords: [23.4700, 85.5600] },
        { name: "Betla National Park", coords: [23.8500, 84.2000] },
        { name: "Netarhat", coords: [23.4700, 84.2700] },
        { name: "Patratu Valley", coords: [23.6800, 85.2800] },
        { name: "Baidyanath Temple (Deoghar)", coords: [24.4800, 86.7000] },
        { name: "Parasnath Hill (Shikharji)", coords: [23.9200, 86.1500] }
      ];

      sites.forEach(site => {
        L.marker(site.coords).addTo(map)
          .bindPopup(`<a href="https://www.google.com/maps?q=${site.coords[0]},${site.coords[1]}" target="_blank">${site.name}</a>`);
      });
    });"""

map_new = """    // --------- Map (Leaflet + OSM) ----------
    document.addEventListener("DOMContentLoaded", function () {
      if (typeof L === 'undefined') {
        console.warn('Leaflet failed to load. Skipping map initialization.');
        return;
      }
      try {
        // Initialize map
        var map = L.map('map').setView([23.6102, 85.2799], 7);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Add markers with clickable links to Google Maps
        const sites = [
          { name: "Hundru Falls", coords: [23.6355, 85.3096] },
          { name: "Jonha Falls", coords: [23.3700, 85.3300] },
          { name: "Dassam Falls", coords: [23.4700, 85.5600] },
          { name: "Betla National Park", coords: [23.8500, 84.2000] },
          { name: "Netarhat", coords: [23.4700, 84.2700] },
          { name: "Patratu Valley", coords: [23.6800, 85.2800] },
          { name: "Baidyanath Temple (Deoghar)", coords: [24.4800, 86.7000] },
          { name: "Parasnath Hill (Shikharji)", coords: [23.9200, 86.1500] }
        ];

        sites.forEach(site => {
          L.marker(site.coords).addTo(map)
            .bindPopup(`<a href="https://www.google.com/maps?q=${site.coords[0]},${site.coords[1]}" target="_blank">${site.name}</a>`);
        });
      } catch (e) {
        console.error('Error initializing map:', e);
      }
    });"""

html = html.replace(book_guide_old, book_guide_new)
html = html.replace(book_transport_old, book_transport_new)
html = html.replace(make_plan_old, make_plan_new)
html = html.replace(map_old, map_new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated js code!")
