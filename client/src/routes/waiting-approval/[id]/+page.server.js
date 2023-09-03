import { API_AWAITING_PROJECTS } from '$lib/consts';

/** @type {import('./$types').PageServerLoad} */
export async function load({ params,fetch }) {
    // fetch data from server
    let url = `${API_AWAITING_PROJECTS}${params.id}/`;
    console.log('fetching awaiting project data from server', url);
    const res = await fetch(url);
    const data = await res.json();
    // return data to be passed to page
    return { project_data: data };
};

