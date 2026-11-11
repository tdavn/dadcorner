    (function() {
      // ----- initialise AOS -----
      AOS.init({
        duration: 800,
        once: true,
        offset: 60,
      });

      // ----- GALLERY POPUP LOGIC -----
      const galleryItems = document.querySelectorAll('.gitem');
      const galPop = document.getElementById('galPop');
      const gpImg = document.getElementById('gpImg');
      const gpTitle = document.getElementById('gpTitle');
      const gpDesc = document.getElementById('gpDesc');
      const gpClose = document.getElementById('gpClose');
      const gpPrev = document.getElementById('gpPrev');
      const gpNext = document.getElementById('gpNext');

      // Build an array with all gallery data (preserving order)
      const galleryData = Array.from(galleryItems).map((item, index) => {
        return {
          index: index,
          img: item.getAttribute('data-gimg'),
          title: item.getAttribute('data-gtitle'),
          desc: item.getAttribute('data-gdesc')
        };
      });

      let currentIndex = 0;        // currently displayed item index
      let isPopupOpen = false;

      // ----- open popup with data at given index -----
      function openPopup(index) {
        if (index < 0) index = galleryData.length - 1;
        if (index >= galleryData.length) index = 0;
        currentIndex = index;

        const data = galleryData[currentIndex];
        gpImg.src = data.img;
        gpTitle.textContent = data.title;
        gpDesc.textContent = data.desc;

        // Show popup using class
        galPop.classList.add('show');
        isPopupOpen = true;

        // Prevent body scrolling when popup is open
        document.body.style.overflow = 'hidden';
      }

      // ----- close popup -----
      function closePopup() {
        galPop.classList.remove('show');
        isPopupOpen = false;
        document.body.style.overflow = '';
        // Clear source to avoid blinking on next open (optional)
        // gpImg.src = '';
      }

      // ----- navigate prev / next -----
      function goPrev() {
        if (!isPopupOpen) return;
        currentIndex = (currentIndex - 1 + galleryData.length) % galleryData.length;
        const data = galleryData[currentIndex];
        gpImg.src = data.img;
        gpTitle.textContent = data.title;
        gpDesc.textContent = data.desc;
      }

      function goNext() {
        if (!isPopupOpen) return;
        currentIndex = (currentIndex + 1) % galleryData.length;
        const data = galleryData[currentIndex];
        gpImg.src = data.img;
        gpTitle.textContent = data.title;
        gpDesc.textContent = data.desc;
      }

      // ----- attach click listeners to each gallery item -----
      galleryItems.forEach((item, idx) => {
        item.addEventListener('click', function(e) {
          e.stopPropagation();   // avoid any weird bubbling
          openPopup(idx);
        });
      });

      // ----- popup controls -----
      gpClose.addEventListener('click', closePopup);
      gpPrev.addEventListener('click', goPrev);
      gpNext.addEventListener('click', goNext);

      // ----- close when clicking on backdrop (galPop itself) -----
      galPop.addEventListener('click', function(e) {
        if (e.target === galPop) {
          closePopup();
        }
      });

      // ----- keyboard: ESC to close, arrows to navigate -----
      document.addEventListener('keydown', function(e) {
        if (!isPopupOpen) return;
        if (e.key === 'Escape') {
          closePopup();
        } else if (e.key === 'ArrowLeft') {
          goPrev();
        } else if (e.key === 'ArrowRight') {
          goNext();
        }
      });

      // optional: stop clicks inside gpbox from closing via backdrop
      document.querySelector('.gpbox').addEventListener('click', function(e) {
        e.stopPropagation();
      });

    })();