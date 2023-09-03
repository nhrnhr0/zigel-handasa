
import { API_NAVBAR } from '$lib/consts';
/** @type {import('./$types').PageServerLoad} */
export async function load({ params,fetch }) {
    // fetch data from server
    let url = `${API_NAVBAR}/`;
    console.log('fetching navbar data from server', url);
    const nav_res = await fetch(url);
    const nav_data = await nav_res.json();
    // return data to be passed to page
    return { nav_data: nav_data };

}