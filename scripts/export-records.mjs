import fs from "node:fs/promises";
import { loadContent, archiveText } from "./archive-content.mjs";

const { records } = await loadContent();
const output = new URL("../public/archives/", import.meta.url);
await fs.mkdir(output, { recursive: true });
for (const record of records)
  await fs.writeFile(
    new URL(`SPACE-FIELD-${record.id}.txt`, output),
    archiveText(record),
    "utf8",
  );
console.log(`Prepared ${records.length} downloadable archive records.`);

const projectOutput = new URL("../public/projects/", import.meta.url);
await fs.mkdir(projectOutput, { recursive: true });
for (const r of records) {
  const imageUrl = r.image.startsWith("/") ? `..${r.image}` : r.image;
  const markdown = `# ${r.title}\n\n${r.en} · ${r.id}\n\n> 概念占位项目，图像为示意，不代表真实委托或已建成作品。\n\n![${r.imageAlt}](${imageUrl})\n\n- 分类：${r.category}\n- 时间：${r.date}\n- 个人职责：${r.lead}\n- 工具：${r.tools}\n${r.video ? `- 视频：${r.video}\n` : ""}\n## 项目概述\n\n${r.abstract}\n\n## 设计过程\n\n${r.findings.join("\n\n")}\n`;
  await fs.writeFile(new URL(`${r.id}.md`, projectOutput), markdown, "utf8");
}
