// function to filter foods based on the tags in the select
document.addEventListener("DOMContentLoaded", function() {
    const selectBox = document.querySelector(".select-box");
    const currentElement = selectBox.querySelector(".select-box__current");
    const squares = document.querySelectorAll(".square");

    currentElement.addEventListener("click", function() {
        const listElement = selectBox.querySelector(".select-box__list");
        listElement.classList.toggle("visible");
    });

    const options = selectBox.querySelectorAll(".select-box__option");
    options.forEach(option => {
        option.addEventListener("click", function() {
            const selectedValue = this.getAttribute("for");
            const radioButton = document.getElementById(selectedValue);
            radioButton.checked = true;
            const selectedText = this.textContent;
            currentElement.querySelector(".select-box__input-text").textContent = selectedText;
            filterRecipes(selectedValue);
            selectBox.querySelector(".select-box__list").classList.remove("visible");
        });
    });

    function filterRecipes(selectedTag) {
        squares.forEach(square => {
            const tags = square.getAttribute("data-tags") ? square.getAttribute("data-tags").split(", ") : [];
            if (selectedTag === "all") {
                square.parentElement.style.display = "block";
            } else {
                if (tags.includes(selectedTag)) {
                    square.parentElement.style.display = "block";
                } else {
                    square.parentElement.style.display = "none";
                }
            }
        });
    }
});
