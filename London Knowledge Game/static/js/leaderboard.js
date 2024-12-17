document.addEventListener("DOMContentLoaded", () => {
    // Only show leaderboard if property_index == 0
    if (typeof propertyIndex !== 'undefined' && propertyIndex === 0) {
        fetch("/leaderboard_data")
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("#leaderboard-table tbody");
            tbody.innerHTML = "";
            data.forEach(entry => {
                const tr = document.createElement("tr");
                const playerNameTd = document.createElement("td");
                playerNameTd.textContent = entry.player_name;
                const agencyTd = document.createElement("td");
                agencyTd.textContent = entry.agency;
                const scoreTd = document.createElement("td");
                scoreTd.textContent = entry.score.toFixed(1);

                tr.appendChild(playerNameTd);
                tr.appendChild(agencyTd);
                tr.appendChild(scoreTd);
                tbody.appendChild(tr);
            });
        });

        const playNowButton = document.getElementById("play-now-button");
        playNowButton.addEventListener("click", () => {
            const modal = document.getElementById("leaderboard-modal");
            modal.style.display = "none";
        });
    }
});
