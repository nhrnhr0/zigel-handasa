
import { API_AWAITING_PROJECTS,API_PROJECTS, BASE_SERVER_URL } from '$lib/consts';
    import {API_ACCOUNTING_DOCS_GET_MORNING_INFO} from '$lib/consts';

export async function network_get_project_accounting_docs(project_id) {
    console.log('network_get_project_accounting_docs');
    let res = await fetch(`${API_PROJECTS}${project_id}/accounting-docs/`, {method: 'GET',});
    return res;
}

export async function network_get_overdue_awaiting_projects() {
    console.log('network_get_overdue_awaiting_projects');
    let res = await fetch(`${API_AWAITING_PROJECTS}?overdue=true`, {method: 'GET',});
    return res;
}

export async function network_create_invoice_from_price_proposals(invoice_data) {
    console.log('network_create_invoice');
    let res = await fetch(`${BASE_SERVER_URL}/create-invoice/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(invoice_data)
    });
    return res;
}
export async function network_create_cancel_invoice_from_invoice(invoice_data) {
    console.log('network_create_cancel_invoice_from_invoice');
    let res = await fetch(`${BASE_SERVER_URL}/create-cancel-invoice/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(invoice_data)
    });
    return res;
}

export async function network_get_morning_info(ids) {
    console.log('network_get_morning_info');
    let url = `${API_ACCOUNTING_DOCS_GET_MORNING_INFO}`;
    if (ids) {
        url += `?morning_ids[]=${ids}`;
    }
    let res =await fetch(url, {method: 'GET',});
    return res;
}

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


export async function network_snooze_awaiting_project(project_id, number_of_days) {
    console.log('network_snooze_project');
    let res =await fetch(`${API_AWAITING_PROJECTS}${project_id}/snooze/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({number_of_days:number_of_days})
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