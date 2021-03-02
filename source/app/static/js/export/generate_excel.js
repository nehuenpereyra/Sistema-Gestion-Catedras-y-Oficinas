function get_excel(data, report_type_name) {
  var wb = XLSX.utils.book_new();
  var today = new Date();
  wb.Props = {
    Title: "Reporte de " + report_type_name,
    Subject: "Fecha: " + today.toLocaleDateString("es-AR"),
    CreatedDate: today,
  };

  wb.SheetNames.push("Reporte de " + report_type_name);

  var ws_data = [];
  var merge = [];
  var index = 0;

  /* Generar tabla */
  ws_data.push(data["fields"]);
  for (const property in data.contents) {
    for (let value of data.contents[property]) {
      ws_data.push(value);
    }
  }

  var ws = XLSX.utils.aoa_to_sheet(ws_data);
  var wscols = [];
  var i;

  /* Establecer la hoja */
  wb.Sheets["Reporte de " + report_type_name] = ws;

  /* Establecer el ancho de las columnas */
  for (i = 0; i < data["fields"].length; i++) {
    wscols.push({ wch: 30 });
  }
  ws["!cols"] = wscols;

  /* Exportar en XLSX */
  var wbout = XLSX.write(wb, { bookType: "xlsx", type: "binary" });
  saveAs(
    new Blob([s2ab(wbout)], { type: "application/octet-stream" }),
    "Reporte de " +
      report_type_name +
      " " +
      today.toLocaleDateString("es-AR") +
      ".xlsx"
  );
}

function s2ab(s) {
  var buf = new ArrayBuffer(s.length);
  var view = new Uint8Array(buf);
  for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xff;
  return buf;
}
