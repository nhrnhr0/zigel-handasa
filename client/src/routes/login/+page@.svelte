<script>
	let username
    let password
    import { goto } from '$app/navigation';
    import { BASE_SERVER_URL } from '../../lib/consts';
 async function login(){
    try {
        const loginData =new FormData()
        loginData.append("userName",username)
        loginData.append("password",password)
        const response = await fetch(`${BASE_SERVER_URL}/login`,{
            method:"POST",
            body:loginData
        }
        );
        if (response.ok) {
			const data = await response.json();
			if(data!="user does not exists"){
				localStorage.setItem("token",data.token)
				goto("/waiting-approval")
			}
			else{
				alert("אחד או יותר מהשדות לא נכון")
			}
        } else {
            console.error('login failed');
        }
        } catch (error) {
        console.error(error);
    }   
}
</script>

<div id="main-container">
    <form id="login-form" on:submit={login}>
        <h1>התחברות</h1>
        <div class="input-container">
            <h3> שם משתמש:</h3>
            <input type="text" class="login-input" bind:value={username} placeholder="admin">
        </div>
        <div class="input-container">
            <h3>סיסמה:</h3>
            <input type="password" class="login-input" bind:value={password} placeholder="admin">
        </div>
        <button type="submit" id="submit-btn">התחבר</button>
    </form>
</div>


<style>
#main-container {
    background: linear-gradient(135deg, #3498db, #6c5ce7);
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

/* Style the login container */
#login-form {
    background-color: rgba(255, 255, 255, 0.95); /* Slightly transparent white background */
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.5);
    text-align: center; /* Center the content horizontally */
    max-width: 400px; /* Limit the width of the login form */
}

/* Style the input container */
.input-container {
    margin-bottom: 20px;
}

/* Style the input fields */
.login-input {
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    font-size: 1rem;
}

.login-input:focus {
    border-color: #4CAF50;
    outline: none;
}

/* Style the headings */
h1 {
    font-size: 2rem;
}

h3 {
    font-size: 1rem;
    margin-bottom: 5px;
}

/* Style the submit button */
#submit-btn {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1.2rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

#submit-btn:hover {
    background-color: #45a049;
}

</style>
