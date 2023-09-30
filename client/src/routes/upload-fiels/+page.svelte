<script>
  import { onMount } from 'svelte';
  import EditComponent from './editComponent.svelte';
  let files;
  let file;
  const SERVERPATH="http://127.0.0.1:8000"
  export let project_id 
  async function uploadFile() {
    const fileData= new FormData()
    fileData.append("file",file[0])
    fileData.append("fileName",file[0].name)
    fileData.append("projectId",project_id)
    const response = await fetch(SERVERPATH+'/files_upload/new', {
      method: 'POST',
      
      body:fileData
     }) .then((response) => response.json())
    .then((data) => {
      // we are setting the names to the names variable
      files = data;
    });
    
    
  }
 


//    onMount( () => {
//       fetch(SERVERPATH+"/files_upload/get/"+project_id)
//     .then((response) => response.json())
//     .then((data) => {
//       files = data;
//     });
// });
onMount(async () => {
    try {
      
      const response = await fetch(`${SERVERPATH}/files_upload/get/${project_id}`);
      if (response.ok) {
        // Assuming the response contains an array of files
        files = await response.json();
      } else {
        console.error('Failed to fetch files:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  });

function makeDownload(){
  
}
</script>
<div id="main-container">

  <!-- {console.log(files)}
  {console.log(project_id)} -->
  {#if files}
    {#each files as file}
    {#if file.file_name.includes("png")||file.file_name.includes("jpg")}
    <div id="img-container">
      <!-- {console.log(file)} -->
      <img   id="image" src={SERVERPATH+file.file} alt={file.file_name}>
      <EditComponent file={file} SERVERPATH={SERVERPATH}/>
    </div>
    {:else if file.file_name.includes("pdf")}
   
      <!-- <iframe src={SERVERPATH+file.file} title={file.file_name}></iframe> -->
      <!-- <embed src={SERVERPATH+file.file} type="application/pdf" width="100%" height="500px"> -->
       
        
    {:else}
    <div id="link-container">
      <a href={SERVERPATH+file.file}  alt={file.file_name}>{file.file_name}</a>
    </div>
    {/if}
    {/each}
  {/if}
</div>

<form on:submit|preventDefault={uploadFile}>
  <input type="file" bind:files={file} />
  <button type="submit">Upload</button>
</form>

<style>
  #image{
    max-height: 30vh;
    max-width: 30vw;
  }
  #img-container{
    min-height: 30vh;
    min-width: 30vw;
  }
  #main-container{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
</style>