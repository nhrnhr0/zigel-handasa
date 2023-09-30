<script>
    export let file
    export let SERVERPATH
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
    const response = await fetch(SERVERPATH+'/files_upload/new', {
      method: 'POST',
      
      body:fileData
     }) .then((response) => response.json())
    .then((data) => {
      // we are setting the names to the names variable
      files = data;
    });
}
</script>
<div>
    <button>
        הורד
    </button>
    <button on:click={delteFile(file)}>
        מחק
    </button>
    <button on:click={getFile(SERVERPATH+file.file)}>
        צפה
    </button>
</div>
<style>

</style>