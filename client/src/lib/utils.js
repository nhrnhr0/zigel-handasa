export function convert_to_money(amount) {
    let value = new Intl.NumberFormat('he-IL', {
		style: 'currency',
		currency: 'ILS',
		minimumFractionDigits: 0,
		maximumFractionDigits: 2
	}).format(amount);
    return value;
}

export function get_hebrew_datetime(date) {
    let value = new Intl.DateTimeFormat('he-IL', {
        dateStyle: 'full',
        timeStyle: 'short'
    }).format(date);
    return value;
}

export function get_hebrew_date(date) {
    debugger;
    if(date === undefined) return '';
    console.log(date)
    try{ 
        let value = new Intl.DateTimeFormat('he-IL', {
        }).format(new Date(date));
        return value;
    }
    catch(e){
        console.log(e);
        return e;
    }
    
}