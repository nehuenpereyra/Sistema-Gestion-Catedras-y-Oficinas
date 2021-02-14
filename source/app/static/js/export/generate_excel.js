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
  for (const property in data.contents) {
    ws_data.push([`${property}`, "", ""]);
    merge.push({
      s: { r: index, c: 0 },
      e: { r: index, c: data["fields"].length - 1 },
    });
    ws_data.push(data["fields"]);
    for (let value of data.contents[property]) {
      ws_data.push(value);
    }
    ws_data.push(["", "", ""]);
    index = index + data.contents[property].length + 3;
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

  /* Establcer los merges entra las filas correspondientes */
  if (!ws["!merges"]) ws["!merges"] = [];
  ws["!merges"] = merge;

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

  /*
  var ws_data = [];
  var merge = [];
  var index = 0;

  for (const property in data.contents) {
    console.log(`${property}: ${data.contents[property]}`);
    ws_data.push([`${property}`, "", ""]);
    merge.push({
      s: { r: index, c: 0 },
      e: { r: index, c: data["fields"].length - 1 },
    });
    ws_data.push(data["fields"]);
    for (let value of data.contents[property]) {
      ws_data.push(value);
    }
    ws_data.push(["", "", ""]);
    index = index + data.contents[property].length + 3;
  }

  console.log(ws_data);
  console.log(merge);
*/

  /* merge cells A1:C1 */
  //var merge = XLSX.utils.decode_range("A1:C1");
  /*
  var merge = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: 2 } },
    { s: { r: 4, c: 0 }, e: { r: 4, c: 2 } },
  ];*/

  /* Establecer el ancho de las columnas 
  var wscols = [{ wch: 30 }, { wch: 30 }, { wch: 30 }];
  ws["!cols"] = wscols;*/

  // this is equivalent var merge = { s: {r:0, c:0}, e: {r:0, c:1} };
  /* add merges 
  if (!ws["!merges"]) ws["!merges"] = [];
  ws["!merges"] = merge;*/
}

function s2ab(s) {
  var buf = new ArrayBuffer(s.length);
  var view = new Uint8Array(buf);
  for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xff;
  return buf;
}
