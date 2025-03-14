document.addEventListener("DOMContentLoaded", function() {
    var canvas = document.getElementById("heartActivityChart");
    if (!canvas) {
        console.error("⚠️ Canvas element 'heartActivityChart' nebyl nalezen!");
        return;
    }

    var dataElement = document.getElementById("heart-data");
    if (!dataElement) {
        console.warn("⚠️ Žádná data pro graf. Možná nemáte záznamy srdeční aktivity.");
        return;
    }

    try {
        var jsonData = JSON.parse(dataElement.textContent);
        var casove_razitka = jsonData.casove_razitka;
        var hodnoty_srdce = jsonData.hodnoty_srdce;

        if (casove_razitka.length === 0 || hodnoty_srdce.length === 0) {
            console.warn("⚠️ Načteno prázdné pole pro graf.");
            return;
        }

        var ctx = canvas.getContext("2d");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: casove_razitka,
                datasets: [{
                    label: "Srdeční aktivita (BPM)",
                    data: hodnoty_srdce,
                    borderColor: "red",
                    fill: false,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: "top"
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Čas"
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Hodnota BPM"
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("🚨 Chyba při načítání dat grafu:", error);
    }
});