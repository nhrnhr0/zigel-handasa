<script>
    export let file
    import {BASE_SERVER_URL} from '../../lib/consts.js'
    export let  project_id
    import {createEventDispatcher} from 'svelte'
    const dispatch =createEventDispatcher();
 async function getFile(file_url) {
  const url = file_url;
  const fileLink = document.createElement('a');
  fileLink.href = url;
  fileLink.setAttribute('download', ''); 
  document.body.appendChild(fileLink);
  fileLink.click();
  document.body.removeChild(fileLink);
}
async function delteFile(file){
    const userCoinfirm =window.confirm("אתה בטוח שתרצה למחוק?")
    if(userCoinfirm){
    const fileData= new FormData()
    fileData.append("fileId",file.id)
    fileData.append("projectId",project_id)
    fileData.append("action","delete_file")
    const response = await fetch(`${BASE_SERVER_URL}/files_upload/${project_id}`, {
      method: 'POST',
      body:fileData,
      headers:{
        'Authorization': `Token ${token}`
      }
     }) .then((response) => response.json())
    .then((data) => {
      // we are setting the names to the names variable
    //   alert("הקובץ נמחק בהצלחה")
      dispatch('updatedData',data)
    });
    }
}

</script>
<div class="button-container">
    <button class="btn" id="green-btn" on:click={getFile(BASE_SERVER_URL+file.file)}>
        צפה
    </button>
    <button class="btn" id="red-btn" on:click={delteFile(file)}>
        מחק
    </button>
</div>
<style>
    .button-container{
        width: 200px;
        height: 40px;
        display: flex;
        justify-content: space-between;
    }
    .btn{
        border-radius: 7px;
        display: flex;
        justify-content: center;
        align-items:center ;
        color: white;
        width: 70px;
    }
    .btn:hover{
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }
    #red-btn{
        background-color:  #f44336;
    }
    #green-btn{
        background-color: #4CAF50;
    }
</style>