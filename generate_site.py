import pandas as pd
import os
import shutil

# --- CONFIGURATION ---
CSV_FILE = "filament_data.csv"
OUTPUT_DIR = "docs"
MY_TAG = "robertk4-20"  # Your Amazon ID

# Mapping 'Affiliate_Key' to actual search URLs
AFFILIATE_LINKS = {
    "pla_generic": f"https://amazon.com/s?k=hatchbox+pla+1.75&tag={MY_TAG}",
    "petg_generic": f"https://amazon.com/s?k=overture+petg+filament&tag={MY_TAG}",
    "tpu_generic": f"https://amazon.com/s?k=ninjaflex+tpu&tag={MY_TAG}",
    "bambu_pla": f"https://amazon.com/s?k=bambu+lab+pla+cf&tag={MY_TAG}",
    "abs_generic": f"https://amazon.com/s?k=sunlu+abs+filament&tag={MY_TAG}",
    "petg_prusa": f"https://amazon.com/s?k=prusament+petg&tag={MY_TAG}"
}

def generate():
    # 1. Load Data
    df = pd.read_csv(CSV_FILE)
    
    # 2. Reset Output Directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 3. Generate Index (Homepage)
    index_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Filament Settings Database</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
    </head>
    <body>
        <h1>🖨️ Filament Settings DB</h1>
        <p>Stop clogging your nozzle. Validated settings for Ender 3, Bambu, and Prusa.</p>
        <input type="text" id="search" onkeyup="filterTable()" placeholder="Search for printer or material...">
        
        <table id="dataTable">
            <thead>
                <tr>
                    <th>Printer</th>
                    <th>Material</th>
                    <th>Brand</th>
                    <th>Nozzle (&deg;C)</th>
                    <th>Bed (&deg;C)</th>
                    <th>Notes</th>
                    <th>Buy</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for _, row in df.iterrows():
        link_key = row['Affiliate_Key']
        buy_link = AFFILIATE_LINKS.get(link_key, "#")
        
        index_html += f"""
        <tr>
            <td><strong>{row['Printer']}</strong></td>
            <td>{row['Material']}</td>
            <td>{row['Brand']}</td>
            <td>{row['Nozzle_Temp']}</td>
            <td>{row['Bed_Temp']}</td>
            <td>{row['Notes']}</td>
            <td><a href="{buy_link}" target="_blank"> Check Price &rarr;</a></td>
        </tr>
        """

    index_html += """
            </tbody>
        </table>
        
        <script>
        function filterTable() {
            var input, filter, table, tr, td, i, txtValue;
            input = document.getElementById("search");
            filter = input.value.toUpperCase();
            table = document.getElementById("dataTable");
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td")[0];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }       
            }
        }
        </script>
    </body>
    </html>
    """
    
    with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    
    print(f"DONE! Generated site in '{OUTPUT_DIR}' with {len(df)} settings.")

if __name__ == "__main__":
    generate()
