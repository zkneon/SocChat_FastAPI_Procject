document.addEventListener("DOMContentLoaded", function(){
        let btn = document.querySelector('input[type=submit]');
        btn.addEventListener('click', async function(event){
            event.preventDefault();
            let data = {
                "grant_type": "",
                "username": document.querySelector('input[name=email]').value,
                "password": document.querySelector('input[name=pass]').value,
                "scope": "",
                "client_id": "",
                "client_secret": "",
            };
            console.log(data)
            let response = await fetch("/auth/login", {
                headers: {"Content-type": "application/x-www-form-urlencoded"},
                method: "POST",
                body: new URLSearchParams(data),
            });
            try{
                let response_json = await response.json();
                console.log(response_json);
                let error_block = document.querySelector('#erorr-msg');
                error_block.style.display = "block";
                if (response_json["detail"] == "LOGIN_BAD_CREDENTIALS") {
                    error_block.innerHTML = "Sorry wrong email or password";
                }

            } catch (e) {
                console.error(e)

            }
            console.log(response);


            if (response.ok){
                let error_block = document.querySelector('#erorr-msg');
                error_block.style.display = "block";
                error_block.classList.replace("alert-danger", "alert-success")
                error_block.innerHTML = "Login Success";
                setTimeout(() => location.href = "/postfeed", 1000);


            }

        })
    })