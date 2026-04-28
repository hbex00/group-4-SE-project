// Getting all the categories
const tag_cat_list = document.querySelectorAll(".dropdown");

tag_cat_list.forEach(btn => {
    // Getting the list of tags inside that category
    const cat_specific_table = btn.querySelectorAll("li");

    // On click changing the input to the li item clicked 
    cat_specific_table.forEach(li_element => {
        li_element.addEventListener("click", () => {
            const string = btn.querySelector("input").placeholder + ": " +li_element.innerText;
            btn.querySelector("input").value = string;
            btn.querySelector('input[type="hidden"]').value = string;
        });
    });
});