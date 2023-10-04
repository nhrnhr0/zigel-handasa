<script>
    let username
    let password
 async function login(){
    
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
        <button type="submit">התחבר</button>
    </form>
</div>

<style>
    #main-container{
        display: flex;
        flex-direction: column;
        height: 50vh;
        width: 100vw;
        align-items: center;
        justify-content: center;
    }
    #login-form{
        height: 45vh;
        width: 35vw;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        border-radius: 10px;
        background-color: rgb(169, 197, 198);
    }
</style>