const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  LevelFormat, PageNumber, Footer, Header,
} = require("docx");
const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "../reports/Cafe_Performance_Analysis_Report.docx");

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cell = (text, bold = false, shade = null, align = AlignmentType.LEFT) =>
  new TableCell({
    borders,
    width: { size: 2340, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [
      new Paragraph({
        alignment: align,
        children: [new TextRun({ text, bold, size: 20, font: "Arial" })],
      }),
    ],
  });

const wideCell = (text, bold = false, shade = null, width = 4680) =>
  new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text, bold, size: 20, font: "Arial" })] })],
  });

const h = (text, level) =>
  new Paragraph({ heading: level, children: [new TextRun({ text, font: "Arial" })] });

const p = (text, spacing = 160) =>
  new Paragraph({
    spacing: { after: spacing },
    children: [new TextRun({ text, size: 22, font: "Arial" })],
  });

const bullet = (text) =>
  new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 100 },
    children: [new TextRun({ text, size: 22, font: "Arial" })],
  });

const headerRow = (cells) =>
  new TableRow({ children: cells, tableHeader: true });

const dataRow = (cells) => new TableRow({ children: cells });

// ── Table helpers ──────────────────────────────────────────────────────────────
const HEADER_COLOR = "D5E8F0";
const ALT_COLOR    = "F5F5F5";

function makeTable(colWidths, rows) {
  return new Table({
    width: { size: colWidths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: colWidths,
    rows,
  });
}

// ── Document ───────────────────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      }],
    }],
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1F3864" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2E74B5" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 },
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "404040" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 },
      },
    ],
  },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E74B5", space: 1 } },
            children: [
              new TextRun({ text: "Local Café Performance Analysis  |  2024 Annual Report", size: 18, color: "555555", font: "Arial" }),
            ],
          }),
        ],
      }),
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            border: { top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC", space: 1 } },
            children: [
              new TextRun({ text: "Page ", size: 18, color: "888888", font: "Arial" }),
              new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "888888", font: "Arial" }),
              new TextRun({ text: " of ", size: 18, color: "888888", font: "Arial" }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, color: "888888", font: "Arial" }),
            ],
          }),
        ],
      }),
    },
    children: [

      // ── COVER / TITLE ──────────────────────────────────────────────────────
      new Paragraph({
        spacing: { before: 1440, after: 200 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "☕  Local Café Performance Analysis", bold: true, size: 56, font: "Arial", color: "1F3864" })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 },
        children: [new TextRun({ text: "2024 Annual Insights Report", size: 32, font: "Arial", color: "2E74B5" })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 },
        children: [new TextRun({ text: "Tools: Google Sheets · SQLite · Python (pandas, matplotlib)", size: 22, font: "Arial", color: "777777" })],
      }),

      // ── EXECUTIVE SUMMARY ──────────────────────────────────────────────────
      h("1. Executive Summary", HeadingLevel.HEADING_1),
      p("This report summarises a data-driven performance analysis of a local café, drawing on 2,200 point-of-sale transactions recorded throughout the 2024 calendar year. The goal was to surface actionable insights on peak trading hours, top-performing products, payment behaviour, and — most importantly — the revenue differential between weekday and weekend trading."),
      p("Key headline findings:"),
      bullet("Total 2024 revenue: $18,802 across 2,200 transactions"),
      bullet("Average transaction value: $8.55 (weekends: $10.08 vs. weekdays: $7.96)"),
      bullet("Weekend transactions generate ~27% higher average spend per visit"),
      bullet("Weekend days account for 28% of transactions but a disproportionate share of high-value orders"),
      bullet("Morning peak (8–10 AM) drives ~34% of all daily traffic"),
      bullet("Coffee dominates revenue at ~40% category share; Food is the second largest at ~36%"),
      bullet("Latte is the single best-selling product (408 units, $1,836 revenue)"),
      new Paragraph({ spacing: { after: 240 } }),

      // ── DATA & METHODOLOGY ────────────────────────────────────────────────
      h("2. Data & Methodology", HeadingLevel.HEADING_1),
      h("2.1 Data Sources", HeadingLevel.HEADING_2),
      p("Three structured datasets were compiled and loaded into a relational database:"),
      makeTable([2800, 6560], [
        headerRow([wideCell("Table", true, HEADER_COLOR, 2800), wideCell("Description", true, HEADER_COLOR, 6560)]),
        dataRow([wideCell("transactions"), wideCell("2,200 rows; one row per sale — timestamp, day type, total, payment method")]),
        dataRow([wideCell("order_items", false, ALT_COLOR), wideCell("4,191 rows; one row per line item — product, category, price", false, ALT_COLOR)]),
        dataRow([wideCell("products"), wideCell("20 rows; product catalogue with category and unit price")]),
      ]),
      new Paragraph({ spacing: { after: 200 } }),
      h("2.2 Analytical Approach", HeadingLevel.HEADING_2),
      p("Data was extracted and stored as CSV files, then loaded into an in-memory SQLite database via Python. Eleven SQL queries covered: overview statistics, peak-hour traffic, product rankings, category performance, weekday vs. weekend breakdowns, weekly trends, payment method mix, and basket-size distribution. Charts were generated with matplotlib and are embedded in the reports/ folder of the project repository."),
      new Paragraph({ spacing: { after: 240 } }),

      // ── KEY FINDINGS ──────────────────────────────────────────────────────
      h("3. Key Findings", HeadingLevel.HEADING_1),

      h("3.1 Peak Trading Hours", HeadingLevel.HEADING_2),
      p("The café experiences two clear footfall surges: a morning rush centred on 8–10 AM (accounting for ~34% of daily transactions) and a secondary lunchtime bump around 12–13 PM (~22% of daily transactions). After 15:00, traffic drops steadily, with minimal activity after 19:00."),
      makeTable([2340, 2340, 2340, 2340], [
        headerRow([cell("Hour", true, HEADER_COLOR), cell("Transactions", true, HEADER_COLOR), cell("Revenue ($)", true, HEADER_COLOR), cell("% of Traffic", true, HEADER_COLOR)]),
        dataRow([cell("08:00"), cell("222"), cell("1,943.25"), cell("10.1%")]),
        dataRow([cell("09:00", false, ALT_COLOR), cell("270", false, ALT_COLOR), cell("2,334.00", false, ALT_COLOR), cell("12.3%", false, ALT_COLOR)]),
        dataRow([cell("10:00"), cell("257"), cell("2,317.75"), cell("11.7%")]),
        dataRow([cell("12:00", false, ALT_COLOR), cell("269", false, ALT_COLOR), cell("2,267.75", false, ALT_COLOR), cell("12.2%", false, ALT_COLOR)]),
      ]),
      new Paragraph({ spacing: { after: 200 } }),

      h("3.2 Top Products", HeadingLevel.HEADING_2),
      p("Coffee beverages dominate the top-10 list by units sold. The Latte is the clear leader both by volume and revenue contribution. Avocado Toast is the standout food item — it ranks 8th by units but generates $1,912 in revenue, the second-highest absolute revenue of any single SKU."),
      makeTable([2600, 1800, 1980, 2980], [
        headerRow([wideCell("Product", true, HEADER_COLOR, 2600), wideCell("Category", true, HEADER_COLOR, 1800), wideCell("Units Sold", true, HEADER_COLOR, 1980), wideCell("Revenue ($)", true, HEADER_COLOR, 2980)]),
        dataRow([wideCell("Latte", false, null, 2600), wideCell("Coffee", false, null, 1800), wideCell("408", false, null, 1980), wideCell("1,836.00", false, null, 2980)]),
        dataRow([wideCell("Espresso", false, ALT_COLOR, 2600), wideCell("Coffee", false, ALT_COLOR, 1800), wideCell("326", false, ALT_COLOR, 1980), wideCell("815.00", false, ALT_COLOR, 2980)]),
        dataRow([wideCell("Americano", false, null, 2600), wideCell("Coffee", false, null, 1800), wideCell("312", false, null, 1980), wideCell("936.00", false, null, 2980)]),
        dataRow([wideCell("Croissant", false, ALT_COLOR, 2600), wideCell("Pastry", false, ALT_COLOR, 1800), wideCell("306", false, ALT_COLOR, 1980), wideCell("918.00", false, ALT_COLOR, 2980)]),
        dataRow([wideCell("Cappuccino", false, null, 2600), wideCell("Coffee", false, null, 1800), wideCell("301", false, null, 1980), wideCell("1,204.00", false, null, 2980)]),
        dataRow([wideCell("Avocado Toast", false, ALT_COLOR, 2600), wideCell("Food", false, ALT_COLOR, 1800), wideCell("225", false, ALT_COLOR, 1980), wideCell("1,912.50", false, ALT_COLOR, 2980)]),
      ]),
      new Paragraph({ spacing: { after: 200 } }),

      h("3.3 Category Revenue Share", HeadingLevel.HEADING_2),
      p("Coffee is the revenue backbone, but Food punches above its weight. Despite having fewer SKUs, the Food category generates 36% of total revenue — largely driven by higher unit prices ($7–9 per item vs. $3–5 for Coffee)."),
      makeTable([2340, 2340, 2340, 2340], [
        headerRow([cell("Category", true, HEADER_COLOR), cell("Units Sold", true, HEADER_COLOR), cell("Revenue ($)", true, HEADER_COLOR), cell("Share (%)", true, HEADER_COLOR)]),
        dataRow([cell("Coffee"), cell("1,953"), cell("7,450.75"), cell("39.6%")]),
        dataRow([cell("Food", false, ALT_COLOR), cell("878", false, ALT_COLOR), cell("6,677.50", false, ALT_COLOR), cell("35.5%", false, ALT_COLOR)]),
        dataRow([cell("Pastry"), cell("728"), cell("2,337.50"), cell("12.4%")]),
        dataRow([cell("Tea", false, ALT_COLOR), cell("371", false, ALT_COLOR), cell("1,205.25", false, ALT_COLOR), cell("6.4%", false, ALT_COLOR)]),
        dataRow([cell("Cold Drink"), cell("261"), cell("1,131.00"), cell("6.0%")]),
      ]),
      new Paragraph({ spacing: { after: 200 } }),

      h("3.4 Weekend Revenue Opportunity", HeadingLevel.HEADING_2),
      p("This is the most commercially significant finding in the analysis. Weekend transactions produce a 27% higher average spend per visit ($10.08 vs. $7.96), and customers purchase more items per visit on weekends (avg. 2.25 items vs. 1.77 on weekdays)."),
      p("Weekend days collectively represent approximately 40% higher revenue opportunity per trading hour when adjusted for customer volume. Projecting this premium across the year suggests that focused weekend programming — extended hours, brunch specials, combo deals — could yield a meaningful uplift in annual revenue."),
      makeTable([2340, 2340, 2340, 2340], [
        headerRow([cell("Day Type", true, HEADER_COLOR), cell("Transactions", true, HEADER_COLOR), cell("Total Revenue ($)", true, HEADER_COLOR), cell("Avg Spend ($)", true, HEADER_COLOR)]),
        dataRow([cell("Weekday"), cell("1,589"), cell("12,642.00"), cell("7.96")]),
        dataRow([cell("Weekend", false, ALT_COLOR), cell("611", false, ALT_COLOR), cell("6,160.00", false, ALT_COLOR), cell("10.08", false, ALT_COLOR)]),
      ]),
      new Paragraph({ spacing: { after: 240 } }),

      // ── RECOMMENDATIONS ───────────────────────────────────────────────────
      h("4. Recommendations", HeadingLevel.HEADING_1),
      h("4.1 Capture the Morning Rush", HeadingLevel.HEADING_2),
      bullet("Ensure full staffing and stocked pastry display by 07:45 AM — the 8–10 AM window generates 34% of daily sales"),
      bullet("Introduce a 'Morning Combo' (coffee + croissant) at a slight discount to increase average basket size"),
      bullet("Pre-batch cold brew and batch-brew filter coffee to reduce wait times at peak"),
      new Paragraph({ spacing: { after: 160 } }),
      h("4.2 Maximise Weekend Revenue", HeadingLevel.HEADING_2),
      bullet("Develop a weekend brunch menu with mid-high margin items (grain bowls, eggs dishes) to build on the existing food revenue strength"),
      bullet("Offer a weekend loyalty stamp — buy 4 items, get a pastry free — to increase items per transaction"),
      bullet("Consider extending Sunday hours to 21:00 as weekend evening data shows untapped demand"),
      new Paragraph({ spacing: { after: 160 } }),
      h("4.3 Grow the Food Category", HeadingLevel.HEADING_2),
      bullet("Food has the second-highest revenue despite fewer SKUs and lower volume — add 2–3 new savoury items to test incremental revenue uplift"),
      bullet("Avocado Toast at $8.50 is a high-revenue single item; promote it prominently and test a premium weekend version"),
      new Paragraph({ spacing: { after: 160 } }),
      h("4.4 Payment & Operations", HeadingLevel.HEADING_2),
      bullet("Card payments account for 59% of transactions — invest in a reliable contactless / tap-to-pay terminal to avoid friction"),
      bullet("Mobile Pay is growing at 16% share; ensure QR code / wallet compatibility is visible at the counter"),
      new Paragraph({ spacing: { after: 240 } }),

      // ── PROJECT NOTES ─────────────────────────────────────────────────────
      h("5. Project Notes", HeadingLevel.HEADING_1),
      p("All data used in this analysis is synthetically generated and does not represent any real business. The dataset was designed to reflect realistic café trading patterns including time-of-day seasonality, product popularity distributions, and a deliberate weekend revenue premium."),
      p("The full project — including raw CSVs, SQL queries, Python analysis script, and chart outputs — is available on GitHub. To reproduce the analysis:"),
      bullet("Clone the repository"),
      bullet("Run:  python scripts/generate_data.py"),
      bullet("Run:  python scripts/analyze.py"),
      p("All charts are saved automatically to the reports/ directory."),

    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(OUT, buffer);
  console.log("Report written to:", OUT);
});
