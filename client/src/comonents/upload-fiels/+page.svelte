<script>
  import { onMount } from 'svelte';
  import EditComponent from './editComponent.svelte';
  import {BASE_SERVER_URL} from '../../lib/consts.js'
  let files;
  let file;
  let formElement
  let isCLicked=null;
  export let project_id 

  async function uploadFile() {
  try {
    const fileData = new FormData();
    
    if (file.length > 1) {
      let fileArr = Array.from(file);
      fileArr.forEach((file) => {
        console.log(file);
        fileData.append("files", file);
        fileData.append('fileNames', file.name);
      });
    } else {
      fileData.append("file", file[0]);
      fileData.append("fileName", file[0].name);
    }
    
    fileData.append("projectId", project_id);

    const response = await fetch(BASE_SERVER_URL + '/files_upload/new', {
      method: 'POST',
      body: fileData,
    });

    if (response.ok) {
      formElement.reset()
      const data = await response.json();
      files = data;
      console.log(file)
    } else {
      console.error('HTTP error:', response.status, response.statusText);
    }
  } catch (error) {
    console.error('Error uploading files:', error);
  }
}
onMount(async () => {
    try {
      const response = await fetch(`${BASE_SERVER_URL}/files_upload/get/${project_id}`);
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


function getDataFromEdit(data){
  files=data.detail;
}
function changeClick(file){
  isCLicked=file===isCLicked?null:file;
}
</script>
<div class="main-container">

  <div>
    <form  bind:this={formElement}>
      <input type="file" bind:files={file} on:change={uploadFile} multiple/>
    </form>
  </div>
  <div id="file-container">

  <!-- {console.log(files)}
    {console.log(project_id)} -->
    {#if files }
    {#each files as file } 
    <!-- {console.log(file)} -->
    <div class="link-container">
      <div id='file' on:click={()=>changeClick(file)}>{file.file_name}</div>
      {#if isCLicked === file}
      <EditComponent  file={file}  project_id={project_id} on:updatedData={getDataFromEdit}/>
      {:else}
      <div class="div1"></div>
      {/if}
    </div>
    {/each}
    {/if}
  </div>
  
</div>

<style>
  .main-container{
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .link-container{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 100px;
    row-gap: 10px;
  }
  .link-container:hover{
    cursor: pointer;
  }
  #file-container{
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
  }
  #file{
    height: 50px;
    width: 200px;
    background-color: rgb(220, 220, 220);
    color: rgb(11, 97, 172);
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  #file:hover{
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  }
  .div1{
    height: 40px;
  }
</style>