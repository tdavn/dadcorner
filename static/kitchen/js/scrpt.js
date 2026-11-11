document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Initialize Animate On Scroll (AOS)
    AOS.init({
        duration: 800,
        once: true,
        offset: 60
    });

    // Handle asynchronous layout corrections for late loading imagery
    window.addEventListener('load', () => {
        AOS.refresh();
    });

    // 2. Select Gallery DOM Elements
    const galleryItems = document.querySelectorAll(".gitem");
    const popup = document.getElementById("galPop");
    const popupImg = document.getElementById("gpImg");
    const popupTitle = document.getElementById("gpTitle");
    const popupDesc = document.getElementById("gpDesc");
    const closeBtn = document.getElementById("gpClose");
    const prevBtn = document.getElementById("gpPrev");
    const nextBtn = document.getElementById("gpNext");

    let currentIndex = 0;

    // Core content updating engine
    const updatePopupContent = (index) => {
        const item = galleryItems[index];
        if (!item) return;

        // Pull data markers straight from HTML attributes
        const imgSrc = item.getAttribute("data-gimg");
        const title = item.getAttribute("data-gtitle");
        const desc = item.getAttribute("data-gdesc");

        popupImg.src = imgSrc;
        popupImg.alt = title;
        popupTitle.innerHTML = title;
        popupDesc.innerHTML = desc;
        
        currentIndex = index;
    };

    // Binding Click Listeners to each grid point
    galleryItems.forEach((item) => {
        item.addEventListener("click", () => {
            const index = parseInt(item.getAttribute("data-gi"), 10);
            updatePopupContent(index);
            popup.classList.add("active");
            document.body.style.overflow = "hidden"; // Prevents underlying page scroll bleed
        });
    });

    // Structural teardown function to close modal
    const closePopup = () => {
        popup.classList.remove("active");
        document.body.style.overflow = ""; // Restores document scroll bar navigation
    };

    closeBtn.addEventListener("click", closePopup);

    // Overlay boundary mask safety dismissals
    popup.addEventListener("click", (e) => {
        if (e.target === popup) closePopup();
    });

    // Cyclical Carousel Logic: Previous Navigation
    prevBtn.addEventListener("click", () => {
        let newIndex = currentIndex - 1;
        if (newIndex < 0) {
            newIndex = galleryItems.length - 1;
        }
        updatePopupContent(newIndex);
    });

    // Cyclical Carousel Logic: Next Navigation
    nextBtn.addEventListener("click", () => {
        let newIndex = currentIndex + 1;
        if (newIndex >= galleryItems.length) {
            newIndex = 0;
        }
        updatePopupContent(newIndex);
    });

    // System Keyboard Shortcuts Mapping (Accessibility Features)
    document.addEventListener("keydown", (e) => {
        if (!popup.classList.contains("active")) return;
        
        if (e.key === "Escape") closePopup();
        if (e.key === "ArrowRight") nextBtn.click();
        if (e.key === "ArrowLeft") prevBtn.click();
    });
});
