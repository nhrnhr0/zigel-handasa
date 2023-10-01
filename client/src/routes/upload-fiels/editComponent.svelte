<script>
    export let file
    export let SERVERPATH
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
    const fileData= new FormData()
    fileData.append("fileId",file.id)
    fileData.append("projectId",project_id)
    const response = await fetch(SERVERPATH+'/files_upload/delete', {
      method: 'POST',
      
      body:fileData
     }) .then((response) => response.json())
    .then((data) => {
      // we are setting the names to the names variable
      dispatch('updatedData',data)
    });
}

</script>
<div>
    <button on:click={downloadFile(file)}>
        הורד
    </button>
    <button on:click={delteFile(file)}>
        מחק
    </button>
    <button on:click={getFile(SERVERPATH+file.file)}>
        צפה
    </button>
    <a href={SERVERPATH+file.file} alt={file.file_name} download={file.file_name}>{file.file_name}</a>
</div>
<style>

</style>