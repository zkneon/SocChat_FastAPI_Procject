document.addEventListener("DOMContentLoaded", function(){
        let btn = document.querySelector('a[id=btn-logout]');
        btn.addEventListener('click', async function(event){
            event.preventDefault();

            let response = await fetch("/auth/logout", {
                headers: {"Accept": "application/json", "Content-type": "application/json"},
                method: "POST",
                body: JSON.stringify(""),
            });

            if (response.ok){
                let error_block = document.querySelector('#erorr-msg');
                error_block.style.display = "block";
                error_block.classList.replace("alert-danger", "alert-success")
                error_block.innerHTML = "Logout Success";
                setTimeout(() => location.href = "/postfeed/lastpost", 2000);


            }

        })
    })