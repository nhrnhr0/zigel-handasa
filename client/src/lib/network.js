
import { API_AWAITING_PROJECTS,API_PROJECTS, BASE_SERVER_URL } from '$lib/consts';

export async function network_update_awaiting_project(project_id, project_data) {
    console.log('network_update_project');
    let res =await fetch(`${API_AWAITING_PROJECTS}${project_id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(project_data)
    });
    return res;
}

export async function network_approve_awaiting_project(project_id,order_number) {
    console.log('network_approve_project');
    let res =await fetch(`${API_AWAITING_PROJECTS}${project_id}/approve/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({order_number:order_number})
    });
    return res;
}
export async function network_reject_awaiting_project(project_id,data) {
    console.log('network_reject_project');
    let res =await fetch(`${API_AWAITING_PROJECTS}${project_id}/reject/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return res;
}

export async function network_update_project(project_id, data) {
    console.log('network_update_project');
    let res =await fetch(`${API_PROJECTS}${project_id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return res;
}

export async function network_get_all_reject_reasons_select(project_id, data) {
    console.log('network_get_reject_reasons_select');
    // 'rejected-projects/reason/'
    let res =await fetch(`${BASE_SERVER_URL}/reject-reasons/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    return res;

}