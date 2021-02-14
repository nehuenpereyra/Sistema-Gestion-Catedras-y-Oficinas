function get_pdf(data, report_type_name) {
  var today = new Date();
  console.log(data);

  jsPDF.autoTableSetDefaults({
    headStyles: { fillColor: "#00889b" },
  });

  /* Se crea el objeto jsPDF con orientación horizontal*/
  var doc = new jsPDF("l");

  var finalY = doc.lastAutoTable.finalY || 10;
  for (const property in data.contents) {
    console.log(`${property}: ${data.contents[property]}`);
    doc.text(`${property}`, 14, finalY + 15);
    doc.autoTable({
      startY: finalY + 20,
      head: [data["fields"]],
      body: data.contents[property],
    });
    finalY = doc.lastAutoTable.finalY;
  }

  doc.autoTable({
    startY: finalY + 20,
    html: ".table",
    useCss: true,
  });

  doc.save(
    "Reporte de " +
      report_type_name +
      " " +
      today.toLocaleDateString("es-AR") +
      ".pdf"
  );
}
