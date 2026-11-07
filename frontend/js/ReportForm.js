document.addEventListener("DOMContentLoaded", () => {
    fetch('form.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('modal-container').innerHTML = data;
            setupModalEvents();
        })
        .catch(err => console.error("Error loading form:", err));
});

function setupModalEvents() {
    const modal = document.getElementById('itemModal');
    const btnReport = document.getElementById('btnReportItem');
    const btnClose = document.getElementById('closeFormBtn');
    const itemForm = document.getElementById('itemForm');
    
    const reportTypes = document.querySelectorAll('input[name="reportType"]');
    const formHeader = document.getElementById('formHeader');
    const modalTitle = document.getElementById('modalTitle');
    const modalSubtitle = document.getElementById('modalSubtitle');
    const labelDate = document.getElementById('labelDate');
    const locationWrapper = document.getElementById('locationWrapper');
    const labelLocation = document.getElementById('labelLocation');
    const currentLocationGrp = document.getElementById('currentLocationGrp');
    const currentLocationInput = document.getElementById('currentLocation');
    const submitBtn = document.getElementById('submitBtn');

    btnReport.addEventListener('click', () => {
        modal.classList.add('show');
    });

    btnClose.addEventListener('click', () => {
        modal.classList.remove('show');
        itemForm.reset();
        resetToLostState();
    });

    reportTypes.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'lost') {
                resetToLostState();
            } else {
                setToFoundState();
            }
        });
    });

    function resetToLostState() {
        formHeader.classList.remove('found-header');
        modalTitle.innerText = "Report a Lost Item";
        modalSubtitle.innerText = "Provide as much detail as possible to help find your item.";
        labelDate.innerHTML = 'Date Lost <span class="required">*</span>';
        
        locationWrapper.style.width = "100%";
        labelLocation.innerHTML = 'Last Known Location <span class="required">*</span>';
        
        currentLocationGrp.classList.add('hidden');
        currentLocationInput.removeAttribute('required');
        
        submitBtn.classList.remove('found-btn');
    }

    function setToFoundState() {
        formHeader.classList.add('found-header');
        modalTitle.innerText = "Report a Found Item";
        modalSubtitle.innerText = "Help us return this item to its rightful owner. Please provide clear details.";
        labelDate.innerHTML = 'Date Found <span class="required">*</span>';
        
        locationWrapper.style.width = "auto"; // half width ke liye
        labelLocation.innerHTML = 'Where did you find it? <span class="required">*</span>';
        
        currentLocationGrp.classList.remove('hidden');
        currentLocationInput.setAttribute('required', 'true');
        
        submitBtn.classList.add('found-btn');
    }

    itemForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const type = document.querySelector('input[name="reportType"]:checked').value;
        const itemName = document.getElementById('itemName').value;
        
        console.log(`Khoj Portal -> ${type.toUpperCase()} Item Reported: ${itemName}`);
        
        itemForm.classList.add('hidden');
        const successMsg = document.getElementById('successMessage');
        successMsg.classList.remove('hidden');
        
        setTimeout(() => {
            modal.classList.remove('show');
            itemForm.classList.remove('hidden');
            successMsg.classList.add('hidden');
            itemForm.reset();
            resetToLostState();
        }, 2500);
    });
}
