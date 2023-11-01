

// export const BASE_SERVER_URL = 'https://zigel-admin.ms-global.co.il' //'http://127.0.0.1:8000';
export const BASE_SERVER_URL = import.meta.env.VITE_BASE_SERVER_URL;


export const API_NAVBAR = BASE_SERVER_URL + '/navbar';


export const API_AWAITING_PROJECTS = BASE_SERVER_URL + '/awaiting-projects/';
export const API_AWAITING_PROJECTS_DESCRIPTION = BASE_SERVER_URL + '/awaiting-projects-description/';

export const API_PROJECTS = BASE_SERVER_URL + '/projects/';
export const API_PROJECTS_DESCRIPTION = BASE_SERVER_URL + '/projects-description/';

export const API_DONE_PROJECTS = BASE_SERVER_URL + '/done-projects/';
export const API_DONE_PROJECTS_DESCRIPTION = BASE_SERVER_URL + '/done-projects-description/';

export const API_REJECTED_PROJECT = BASE_SERVER_URL + '/rejected-projects/';
export const API_REJECTED_PROJECT_DESCRIPTION = BASE_SERVER_URL + '/rejected-projects-description/';

export const API_ACCOUNTING_DOCS = BASE_SERVER_URL + '/accounting-docs/';
export const API_ACCOUNTING_DOCS_DESCRIPTION = BASE_SERVER_URL + '/accounting-docs-description/';

export const API_ACCOUNTING_DOCS_GET_MORNING_INFO = BASE_SERVER_URL + '/accounting-docs-morning-info/';

export const API_POSITIVE_CASH_FLOW_INVOICE_DESCRIPTION = BASE_SERVER_URL + '/positive-cash-flow-invoice-description/';
export const API_POSITIVE_CASH_FLOW_INVOICE = BASE_SERVER_URL + '/positive-cash-flow-invoice/';

export const API_POSITIVE_CASH_FLOW_PORJECTS = BASE_SERVER_URL + '/positive-cash-flow-project/';

export const SEARCH_QUERY_PARAM = 'search';
export const ORDERING_QUERY_PARAM = 'ordering';
export const PAGINATION_QUERY_PARAM = 'page';
export const PAGE_SIZE_QUERY_PARAM = 'page_size';