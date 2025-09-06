document.addEventListener('DOMContentLoaded', function() {
    const customerSelect = document.getElementById('customer');
    const departmentSelect = document.getElementById('department');

    if (customerSelect && departmentSelect) {
        customerSelect.addEventListener('change', function() {
            const customerId = this.value;
            departmentSelect.innerHTML = '<option value="">Select a department</option>';

            if (customerId) {
                fetch(`/api/departments?customer_id=${customerId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(department => {
                            const option = document.createElement('option');
                            option.value = department.id;
                            option.textContent = department.name;
                            departmentSelect.appendChild(option);
                        });
                    });
            }
        });
    }
});

