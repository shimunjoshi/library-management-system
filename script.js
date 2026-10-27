const searchInput = document.getElementById("bookSearch");
const booksTable = document.getElementById("booksTable");

if (searchInput && booksTable) {
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim().toLowerCase();
    booksTable.querySelectorAll("tbody tr").forEach((row) => {
      row.hidden = !row.innerText.toLowerCase().includes(query);
    });
  });
}
