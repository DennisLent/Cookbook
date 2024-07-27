// function to filter foods based on the tags in the select
document.addEventListener("DOMContentLoaded", function() {
    const selectElement = document.querySelector(".tag-select");
    const squares = document.querySelectorAll(".square");

    selectElement.addEventListener("change", function() {
        const selectedTag = this.value;
        filterRecipes(selectedTag);
    });

    function filterRecipes(selectedTag) {
        squares.forEach(square => {
            const tags = square.getAttribute("data-tags") ? square.getAttribute("data-tags").split(", ") : [];
            if (selectedTag === "all" || selectedTag === "Show all") {
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
