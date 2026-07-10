
    // -------- Featured Places (images via topic-based Unsplash placeholders) ----------
    const PLACES = [
      {
        name:"Dassam Falls (Ranchi)",
        tag:"Waterfall",
        img:"https://dynamic-media-cdn.tripadvisor.com/media/photo-o/19/fa/bd/6e/a-full-view-of-the-falls.jpg?w=900&h=500&s=1",
        blurb:"A spectacular cascade on the Kanchi River surrounded by sal forests."
      },
      {
        name:"Hundru Falls (Ranchi)",
        tag:"Waterfall",
        img:"https://thumbs.dreamstime.com/b/hundru-waterfalls-jharkhand-287522583.jpg",
        blurb:"Monsoon-favorite plunge pool and scenic rock formations."
      },
      {
        name:"Betla National Park (Palamu)",
        tag:"Wildlife",
        img:"https://superbcollections.com/wp-content/uploads/2023/08/Betla-National-Park.jpeg",
        blurb:"Forests, elephants, and the ruins of Palamu Fort—Jharkhand's classic safari."
      },
      {
        name:"Netarhat",
        tag:"Hill Station",
        img:"https://thumbs.dreamstime.com/b/netarhat-jharkhand-indian-view-pictures-taken-vishal-singh-170710563.jpg",
        blurb:"'Queen of Chotanagpur'—famed for sunrise/sunset points and pine avenues."
      },
      {
        name:"Patratu Valley",
        tag:"Scenic Drive",
        img:"https://media-cdn.tripadvisor.com/media/photo-s/0e/5e/c0/46/drone-shot-of-the-valley.jpg",
        blurb:"Winding roads, emerald hills, and the shimmering Patratu Lake."
      },
      {
        name:"Baidyanath Temple (Deoghar)",
        tag:"Pilgrimage",
        img:"https://cdn1.prayagsamagam.com/media/2023/01/25183337/Baidyanath-Dham-1-1024x576.webp",
        blurb:"One of the 12 Jyotirlingas—vibrant religious hub with old-world charm."
      },
      {
        name:"Parasnath Hill (Shikharji)",
        tag:"Trek",
        img:"https://dynamic-media-cdn.tripadvisor.com/media/photo-o/09/6c/f6/c8/parasnath-hills.jpg?w=1200&h=-1&s=1",
        blurb:"Important Jain pilgrimage; rewarding hikes and misty viewpoints."
      },
      {
        name:"Ranchi Lake & Rock Garden",
        tag:"City",
        img:"https://dynamic-media-cdn.tripadvisor.com/media/photo-o/18/3d/c0/dd/rock-garden.jpg?w=900&h=500&s=1",
        blurb:"Relaxing lakeside vibes and sculpted gardens within the city."
      },
      {
        name:"Tribal Handicrafts",
        tag:"Marketplace",
        img:"https://zineart.in/images/DOK/DOK006011.webp",
        blurb:"Local artisans, dokra metal craft, bamboo works—shop responsibly."
      }
    ];
    const grid = document.getElementById('placeGrid');
    grid.innerHTML = PLACES.map(p => `
      <article class="card">
        <img class="media" src="${p.img}" alt="${p.name}">
        <div class="pad">
          <span class="chip">${p.tag}</span>
          <h3 style="margin:.4rem 0 .3rem">${p.name}</h3>
          <p class="muted">${p.blurb}</p>
        </div>
      </article>
    `).join('');

    // -------- Guide & Transport (localStorage to simulate booking) ----------
    function save(key, payload){
      const arr = JSON.parse(localStorage.getItem(key) || '[]');
      arr.push({...payload, ts: new Date().toISOString()});
      localStorage.setItem(key, JSON.stringify(arr));
    }
    function bookGuide(){
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
    }
    function bookTransport(){
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
    }
    
    // -------- Activity Booking Function ----------
    async function bookActivity() {
      const session = await getSession();
      if (!session) {
        sessionStorage.setItem('redirectAfterLogin', window.location.href);
        window.location.href = '/login';
        return;
      }
      const data = {
        name: document.getElementById('aName').value.trim(),
        phone: document.getElementById('aPhone').value.trim(),
        email: document.getElementById('aEmail').value.trim(),
        activity: document.getElementById('aActivity').value,
        location: document.getElementById('aLocation').value,
        participants: document.getElementById('aParticipants').value,
        date: document.getElementById('aDate').value,
        requirements: document.getElementById('aRequirements').value.trim()
      };
      
      if (!data.name || !data.phone || !data.date || !data.activity) { 
        document.getElementById('aMsg').textContent = "Please fill name, phone, activity and date.";
        document.getElementById('aMsg').style.color = "#ffaaaa"; 
        return; 
      }
      
      // Save to localStorage (simulating booking)
      fetch('/api/book-activity', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      }).then(r => r.json()).catch(e => console.error(e));
      
      document.getElementById('aMsg').textContent = "Activity booking request submitted! We'll confirm within 24 hours.";
      document.getElementById('aMsg').style.color = "#9fe29f";
      
      // Clear form
      document.getElementById('aName').value = '';
      document.getElementById('aPhone').value = '';
      document.getElementById('aEmail').value = '';
      document.getElementById('aActivity').value = '';
      document.getElementById('aLocation').value = '';
      document.getElementById('aParticipants').value = '';
      document.getElementById('aDate').value = '';
      document.getElementById('aRequirements').value = '';
    }

    // --------- Quick itinerary generator ----------
    function makePlan(){
      const days = document.getElementById("days");
      const plan = document.getElementById("plan");
      const d = parseInt(days ? days.value : "1", 10);
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
        out.push(`Day ${i+1}: ${skeleton[i] || "Leisure / shopping / buffer"}\n  • ${daily.join("\n  • ")}`);
      }
      if(plan) plan.textContent = out.join("\n\n");
    }
    function paceSelectValue(){ return document.getElementById('pace')?.value || 'Balanced'; }

    // --------- Map (Leaflet + OSM) ----------
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
    });

    // --------- Improved Chatbot ----------
    function handleChat() {
      const box = document.getElementById('chatInput');
      const lang = document.getElementById('chatLang').value;
      const q = box.value.trim();
      
      if (!q) return;
      
      const log = document.getElementById('chatLog');
      
      // Add user message
      const you = document.createElement('div');
      you.className = 'chat-message user-message';
      you.innerHTML = `<strong>You:</strong> ${q}`;
      log.appendChild(you);
      
      // Process question and generate response
      const response = processQuestion(q, lang);
      
      // Add bot response after a short delay to simulate thinking
      setTimeout(() => {
        const a = document.createElement('div');
        a.className = 'chat-message bot-message';
        a.innerHTML = `<strong>Assistant (${lang}):</strong> ${response}`;
        log.appendChild(a);
        
        // Scroll to bottom
        log.scrollTop = log.scrollHeight;
      }, 600);
      
      // Clear input
      box.value = "";
    }
    
    function processQuestion(question, language) {
      question = question.toLowerCase();
      
      // Weather related questions
      if (question.includes('weather') || question.includes('temperature') || question.includes('rain')) {
        const responses = {
          English: [
            "The weather in Jharkhand is generally pleasant. Currently, it's around 25°C with partly cloudy skies.",
            "Jharkhand has a subtropical climate. Today's forecast shows sunshine with a high of 28°C and a low of 18°C.",
            "This time of year, Jharkhand experiences mild temperatures averaging 22-30°C with low humidity.",
            "The weather is perfect for tourism! Expect clear skies with temperatures around 26°C during the day."
          ],
          Hindi: [
            "झारखंड में मौसम आम तौर पर सुहावना रहता है। वर्तमान में, यह आंशिक रूप से बादलों वाली आसमान के साथ लगभग 25°C है।",
            "झारखंड में उपोष्णकटिबंधीय जलवायु है। आज के पूर्वानुमान में अधिकतम 28°C और न्यूनतम 18°C के साथ धूप दिखाई दे रही है।"
          ],
          Bangla: [
            "ঝাড়খণ্ডের আবহাওয়া সাধারণত মনোরম। বর্তমানে, আংশিক মেঘলা আকাশ সহ প্রায় 25°C।",
            "ঝাড়খণ্ডের একটি উপক্রান্তীয় জলবায়ু রয়েছে। আজকের পূর্বাভাসে সর্বোচ্চ 28°C এবং সর্বনিম্ন 18°C তাপমাত্রার সাথে রোদ দেখাচ্ছে।"
          ]
        };
        return getRandomResponse(responses[language] || responses.English);
      }
      
      // Travel time questions
      else if (question.includes('travel') || question.includes('time') || question.includes('how long') || question.includes('distance')) {
        const responses = {
          English: [
            "Travel times in Jharkhand vary by destination. From Ranchi to most tourist spots, it takes 2-4 hours by road.",
            "Depending on your destination, travel times can range from 1 hour to 5 hours. Could you specify where you're planning to go?",
            "Jharkhand has good road connectivity. Most inter-city travels take 2-3 hours on average.",
            "Travel times depend on your starting point and destination. For example, Ranchi to Dassam Falls is about 2 hours by car."
          ],
          Hindi: [
            "झारखंड में यात्रा का समय गंतव्य के अनुसार अलग-अलग होता है। रांची से अधिकांश पर्यटन स्थलों तक सड़क मार्ग से 2-4 घंटे लगते हैं।",
            "आपके गंतव्य के आधार पर, यात्रा का समय 1 घंटे से 5 घंटे तक हो सकता है। क्या आप बता सकते हैं कि आप कहाँ जाने की योजना बना रहे हैं?"
          ],
          Bangla: [
            "ঝাড়খণ্ডে ভ্রমণের সময় গন্তব্যের উপর নির্ভর করে পরিবর্তিত হয়। রাঁচি থেকে বেশিরভাগ পর্যটন স্পটে, সড়কপথে 2-4 ঘন্টা সময় লাগে।",
            "আপনার গন্তব্যের উপর নির্ভর করে, ভ্রমণের সময় 1 ঘন্টা থেকে 5 ঘন্টা পর্যন্ত হতে পারে। আপনি কি নির্দিষ্ট করতে পারেন যে আপনি কোথায় যাওয়ার পরিকল্পনা করছেন?"
          ]
        };
        return getRandomResponse(responses[language] || responses.English);
      }
      
      // Permit related questions
      else if (question.includes('permit') || question.includes('permission') || question.includes('document')) {
        const responses = {
          English: [
            "For most tourist areas in Jharkhand, no special permits are needed. However, protected areas like certain wildlife sanctuaries require permits.",
            "Generally, Indian nationals don't need permits for tourism in Jharkhand. Foreign nationals should check specific requirements for protected areas.",
            "Permits are required mainly for restricted tribal areas and some national parks. For most tourist spots, no special permits are needed.",
            "You can obtain necessary permits from the Jharkhand Tourism Development Corporation office or online through their portal."
          ],
          Hindi: [
            "झारखंड के अधिकांश पर्यटन क्षेत्रों के लिए, किसी विशेष परमिट की आवश्यकता नहीं है। हालाँकि, कुछ वन्यजीव अभयारण्यों जैसे संरक्षित क्षेत्रों के लिए परमिट की आवश्यकता होती है।",
            "आम तौर पर, भारतीय नागरिकों को झारखंड में पर्यटन के लिए परमिट की आवश্যकता नहीं होती है। विदेशी नागरिकों को संरक्षित क्षेत्रों के लिए विशिष्ट आवश्यकताओं की जांच करनी चाहिए।"
          ],
          Bangla: [
            "ঝাড়খণ্ডের বেশিরভাগ পর্যটন অঞ্চলের জন্য, কোন বিশেষ অনুমতির প্রয়োজন নেই। তবে, কিছু বন্যপ্রাণী অভয়ারণ্যের মতো সংরক্ষিত অঞ্চলগুলির জন্য অনুমতির প্রয়োজন হয়।",
            "সাধারণত, ভারতীয় নাগরিকদের ঝাড়খণ্ডে পর্যটনের জন্য অনুমতির প্রয়োজন নেই। বিদেশী নাগরিকদের সংরক্ষিত অঞ্চলগুলির জন্য নির্দিষ্ট প্রয়োজনীয়তা পরীক্ষা করা উচিত।"
          ]
        };
        return getRandomResponse(responses[language] || responses.English);
      }
      
      // Activities questions
      else if (question.includes('trek') || question.includes('hike') || question.includes('activity') || question.includes('adventure')) {
        const responses = {
          English: [
            "Jharkhand offers excellent trekking opportunities! Popular treks include Parasnath Hill, Netarhat trails, and hikes around Ranchi. Difficulty ranges from easy to challenging.",
            "For adventure activities, try waterfall rappelling at Dassam Falls, rock climbing, or river rafting on the Subarnarekha River. Most activities require booking in advance.",
            "Popular activities include jungle safaris in Betla National Park, tribal village visits, and nature walks. There's something for every adventure level!",
            "Trekking season is best from October to March when the weather is cool. Monsoon season (June-September) is great for waterfall visits but some trails may be slippery."
          ],
          Hindi: [
            "झारखंड शानदार ट्रेकिंग अवसर प्रदान करता है! लोकप्रिय ट्रेक में परसनाथ हिल, नेतरहट ट्रेल और रांची के आसपास की पैदल यात्राएं शामिल हैं। कठिनाई आसान से लेकर चुनौतीपूर्ण तक होती है।",
            "साहसिक गतिविधियों के लिए, दासम फॉल्स पर वॉटरफॉल रैपलिंग, रॉक क्लाइम्बिंग, या स्वर्णरेखा नदी पर रिवर राफ्टिंग आज़माएं। अधिकांश गतिविधियों के लिए अग्रिम बुकिंग की आवश्यकता होती है।"
          ],
          Bangla: [
            "ঝাড়খণ্ড দুর্দান্ত ট্রেকিং সুযোগ প্রদান করে! জনপ্রিয় ট্রেকগুলির মধ্যে রয়েছে পারসনাথ হিল, নেতারহাট ট্রেইল এবং রাঁচির চারপাশের হাইক। অসুবিধা সহজ থেকে চ্যালেঞ্জিং পর্যন্ত হয়।",
            "অ্যাডভেঞ্চার অ্যাক্টিভিটির জন্য, দাসম ফলসে জলপ্রপাত রেপেলিং, রক ক্লাইম্বিং বা সুবর্ণরেখা নদীতে রিভার রাফটিং চেষ্টা করুন। বেশিরভাগ ক্রিয়াকলাপের জন্য আগাম বুকিং প্রয়োজন।"
          ]
        };
        return getRandomResponse(responses[language] || responses.English);
      }
      
      // General tourism questions
      else if (question.includes('place') || question.includes('visit') || question.includes('see') || question.includes('go')) {
        const responses = {
          English: [
            "Jharkhand has many beautiful places to visit! Popular destinations include Dassam Falls, Betla National Park, Hundru Falls, and Jagannath Temple.",
            "You must visit the stunning waterfalls in Jharkhand! Popular ones are Hundru Falls, Dassam Falls, and Jonha Falls. The state is famous for its natural beauty.",
            "I recommend visiting Netarhat, often called the 'Queen of Chotanagpur' for its beautiful sunrises and sunsets. Also don't miss the wildlife at Betla National Park.",
            "Top attractions in Jharkhand include Patratu Valley, Tagore Hill, Rock Garden, and the religious site of Baidyanath Dham. There's something for every type of traveler!"
          ],
          Hindi: [
            "झारखंड में घूमने के लिए कई सुंदर स्थान हैं! लोकप्रिय गंतव्यों में दासम फॉल्स, बेतला राष्ट्रीय उद्यान, हुंडरू फॉल्स और जगन्नाथ मंदिर शामिल हैं।",
            "आपको झारखंड के अद्भुत झरनों को अवश्य देखना चाहिए! हुंडरू फॉल्स और दासम फॉल्स लोकप्रिय हैं।"
          ],
          Bangla: [
            "ঝাড়খণ্ডে দেখার মতো অনেক সুন্দর জায়গা রয়েছে! জনপ্রিয় গন্তব্যগুলির মধ্যে রয়েছে দাসম ফলস, বেতলা জাতীয় উদ্যান এবং হুন্ড্রু ফলস।"
          ]
        };
        return getRandomResponse(responses[language] || responses.English);
      }
      
      // Hello
      else if (question.includes('hello') || question.includes('hi') || question.includes('hey') || question.includes('namaste')) {
        const responses = {
          English: [
            "Hello! How can I assist you with your Jharkhand travel plans today?",
            "Hi there! What would you like to know about Jharkhand tourism?",
            "Namaste! Welcome to Jharkhand Tourism. How can I help you today?"
          ],
          Hindi: [
            "नमस्ते! मैं आज आपकी झारखंड यात्रा की योजनाओं में कैसे सहायता कर सकता हूँ?",
            "नमस्ते! आप झारखंड पर्यटन के बारे में क्या जानना चाहेंगे?"
          ],
          Bangla: [
            "হ্যালো! আজ আমি আপনার ঝাড়খণ্ড ভ্রমণের পরিকল্পনায় কীভাবে সাহায্য করতে পারি?",
            "হাই! আপনি ঝাড়খণ্ড পর্যটন সম্পর্কে কী জানতে চান?"
          ]
        };
        return getRandomResponse(responses[language] || responses.English);
      }
      
      // Thank you
      else if (question.includes('thank')) {
        const responses = {
          English: [
            "You're welcome! Is there anything else you'd like to know about Jharkhand?",
            "Happy to help! Let me know if you have any other questions.",
            "My pleasure! Feel free to ask if you need more information about Jharkhand tourism."
          ],
          Hindi: [
            "आपका स्वागत है! क्या आप झारखंड के बारे में कुछ और जानना चाहेंगे?",
            "मदद करके खुशी हुई! यदि आपके कोई अन्य प्रश्न हैं तो मुझे बताएं।"
          ],
          Bangla: [
            "আপনাকে স্বাগতম! ঝাড়খণ্ড সম্পর্কে আপনি还有什么想知道吗?",
            "সাহায্য করে খুশি! আপনার অন্য কোন প্রশ্ন থাকলে আমাকে জানান।"
          ]
        };
        return getRandomResponse(responses[language] || responses.English);
      }
      
      // Default response for unrecognized questions
      else {
        const responses = {
          English: [
            "I'm not sure I understand. Could you please rephrase your question? I can help with information about travel times, weather, permits, and places to visit in Jharkhand.",
            "I specialize in Jharkhand tourism information. Could you ask about travel times, weather conditions, or permit requirements?",
            "I'm here to help with Jharkhand tourism queries. Try asking about popular destinations, travel information, or weather forecasts.",
            "For accurate information, please ask about Jharkhand's travel conditions, weather, or permit requirements. I'd be happy to help!"
          ],
          Hindi: [
            "मुझे यकीन नहीं है कि मैं समझ पाया। क्या आप कृपया अपना प्रश्न दोबारा कह सकते हैं? मैं झारखंड में यात्रा के समय, मौसम, परमिट और देखने लायक स्थानों के बारे में जानकारी के साथ मदद कर सकता हूँ।",
            "मैं झारखंड पर्यटन सूचना में विशेषज्ञता रखता हूं। क्या आप यात्रा के समय, मौसम की स्थिति, या परमिट आवश्यकताओं के बारे में पूछ सकते हैं?"
          ],
          Bangla: [
            "আমি নিশ্চিত নই যে আমি বুঝতে পেরেছি। আপনি কি আপনার প্রশ্নটি পুনরায় বলতে পারেন? আমি ঝাড়খণ্ডে ভ্রমণের সময়, আবহাওয়া, অনুমতি এবং দেখার জায়গা সম্পর্কে তথ্য দিয়ে সাহায্য করতে পারি।",
            "আমি ঝাড়খণ্ড পর্যটন তথ্যে বিশেষজ্ঞ। আপনি কি ভ্রমণের সময়, আবহাওয়ার অবস্থা, বা অনুমতির প্রয়োজনীয়তা সম্পর্কে জিজ্ঞাসা করতে পারেন?"
          ]
        };
        return getRandomResponse(responses[language] || responses.English);
      }
    }
    
    function getRandomResponse(responses) {
      return responses[Math.floor(Math.random() * responses.length)];
    }

    // footer year
    document.getElementById('yr').textContent = new Date().getFullYear();
  