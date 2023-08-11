document.addEventListener("DOMContentLoaded", function(){
        let btn = document.querySelector('input[type=submit]');
        btn.addEventListener('click', async function(event){
            event.preventDefault();
            let data = {
                "username": document.querySelector('input[name=name]').value,
                "email": document.querySelector('input[name=email]').value,
                "password": document.querySelector('input[name=pass]').value,
                "is_active": true,
                "is_superuser": false,
                "is_verified": false,
                "id": 0,
                "role_id": 0
            };
            let response = await fetch("/auth/register", {
                headers: {"Accept": "application/json", "Content-type": "application/json"},
                method: "POST",
                body: JSON.stringify(data),
            });

            let response_json = await response.json();
            console.log(response);
            console.log(response_json);

            if (response.ok){
                let error_block = document.querySelector('#erorr-msg');
                error_block.style.display = "block";
                error_block.classList.replace("alert-danger", "alert-success")
                error_block.innerHTML = response.statusText;
                setTimeout(() => location.href = "/auth_pages/login", 1000)
            } else {
                let error_block = document.querySelector('#erorr-msg');
                error_block.style.display = "block";
                if (response_json.detail[0]){
                    error_block.innerHTML = response_json.detail[0].msg;
                } else {
                    error_block.innerHTML = response_json.detail.reason;

                }

            }

        })
    })