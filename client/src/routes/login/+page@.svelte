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
    #main-container{
        display: flex;
        flex-direction: column;
        height: 90vh;
        width: 100vw;
        align-items: center;
		background: rgb(2,0,36);
		background: linear-gradient(270deg, rgba(2,0,36,1) 0%, rgba(42,178,184,1) 0%, rgba(0,212,255,1) 100%);
    }
    #login-form{
        height: 45vh;
        width: 500px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        border-radius: 10px;
        background-color: rgb(169, 197, 198);
		position: relative;
		top: 10%;
    }
	#submit-btn{
		border-radius: 10px;
		border-color: none;
		height: 4vh;
		width: 13vw;
		font-size:100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	#submit-btn:hover{
		color: white;
		background-color: #4CAF50;
	}
	.login-input{
		border-radius: 10px;
		height: 4vh;
		width: 13vw;
	}
	h3{
		font-size: 1rem;
	}
	h1{
		font-size: 2rem;
	}
</style>
