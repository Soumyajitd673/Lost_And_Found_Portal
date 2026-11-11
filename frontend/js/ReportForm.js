document.addEventListener("DOMContentLoaded", () => {
    fetch("/item/report_form")
    .then(response => {
        if (!response.ok) {
            throw new Error("Could not load form (" + response.status + ")");
        }
        return response.text();
    })
    .then(html => {
        document.getElementById("modal-container").innerHTML = html;
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
        
        locationWrapper.style.width = "auto";
        labelLocation.innerHTML = 'Where did you find it? <span class="required">*</span>';
        
        currentLocationGrp.classList.remove('hidden');
        currentLocationInput.setAttribute('required', 'true');
        
        submitBtn.classList.add('found-btn');
    }

    itemForm.addEventListener('submit', async(e) => {
        e.preventDefault();
        
        const type = document.querySelector('input[name="reportType"]:checked').value;
        const itemDataObject = {
            title: document.getElementById('itemName').value, 
            description: document.getElementById('itemDescription') ? document.getElementById('itemDescription').value : null,
            category: document.getElementById('itemCategory') ? document.getElementById('itemCategory').value : "Other",
            location: type === 'lost' 
                ? (document.getElementById('itemLocation') ? document.getElementById('itemLocation').value : "Unknown")
                : (document.getElementById('currentLocation') ? document.getElementById('currentLocation').value : "Unknown")
        };
        const formData = new FormData();
        formData.append('item_data', JSON.stringify(itemDataObject));
        
        const imageInput = document.getElementById('itemImage'); 
        if (imageInput && imageInput.files.length > 0) {
            formData.append('image', imageInput.files[0]);
        } else {
            alert("Please upload an image.");
            return;
        }

        // 3. Determine endpoint
        const endpoint = type === 'lost' ? '/item/lost' : '/item/found';

        // 4. Send to FastAPI
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData,
                // Uncomment if you use cookies for get_current_user:
                // credentials: 'include',
            });

            if (response.ok) {
                console.log(`Campus Find -> ${type.toUpperCase()} Item Reported: ${itemDataObject.title}`);
                
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
            } else {
                const errorData = await response.json();
                console.error("Backend Error:", errorData);
                alert("Failed to report item: " + (errorData.detail || "Unknown error"));
            }
        } catch (error) {
            console.error("Network error:", error);
            alert("Could not connect to the server.");
        }
    });
}
