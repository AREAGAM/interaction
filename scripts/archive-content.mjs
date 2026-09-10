import fs from "node:fs/promises";
import { loadWorkbookContent } from "./workbook-content.mjs";

const requiredFields = [
  "id",
  "title",
  "en",
  "department",
  "category",
  "date",
  "lead",
  "clearance",
  "abstract",
  "source",
  "image",
];
const isText = (value) => typeof value === "string" && value.trim().length > 0;

export function validateContent(content) {
  const errors = [];
  if (!content || typeof content !== "object" || Array.isArray(content))
    throw new Error("档案数据必须是对象。");
  for (const key of ["categories", "columns"]) {
    const names = content[key];
    if (!Array.isArray(names) || names.length !== 6 || !names.every(isText))
      errors.push(`${key}：必须包含六个非空分类名称`);
    else if (new Set(names).size !== 6 || names.includes("全部档案"))
      errors.push(`${key}：分类名称不能重复，也不能使用“全部档案”`);
  }
  const categories = Array.isArray(content.categories)
    ? content.categories
    : [];
  const columns = Array.isArray(content.columns) ? content.columns : [];
  if (
    categories.some((name) => !columns.includes(name)) ||
    columns.some((name) => !categories.includes(name))
  )
    errors.push("categories 与 columns 必须包含相同的六个分类");
  const records = Array.isArray(content.records) ? content.records : [];
  if (records.length !== 48) errors.push("records：当前阵列要求四十八份档案");
  const ids = new Set();
  records.forEach((record, index) => {
    const label = `records[${index}]`;
    if (!record || typeof record !== "object" || Array.isArray(record)) {
      errors.push(`${label}：必须是档案对象`);
      return;
    }
    for (const key of requiredFields)
      if (!isText(record[key])) errors.push(`${label}.${key}：必须是非空文本`);
    const expectedId = `X-${String(index + 1).padStart(3, "0")}`;
    if (record.id !== expectedId)
      errors.push(`${label}.id：应为 ${expectedId}，编号须按顺序保持稳定`);
    if (ids.has(record.id)) errors.push(`${label}.id：重复编号 ${record.id}`);
    ids.add(record.id);
    if (!categories.includes(record.category))
      errors.push(`${label}.category：未知分类 ${record.category}`);
    if (
      !Array.isArray(record.findings) ||
      record.findings.length === 0 ||
      !record.findings.every(isText)
    )
      errors.push(`${label}.findings：必须包含至少一条非空研究记录`);
    try {
      const url = new URL(record.source, "https://portfolio.local");
      if (
        !record.source.startsWith("/projects/") &&
        !/^https?:\/\//.test(record.source)
      )
        throw new Error();
      if (!["https:", "http:"].includes(url.protocol)) throw new Error();
    } catch {
      errors.push(`${label}.source：必须是有效的 HTTP 或 HTTPS 链接`);
    }
  });
  for (const name of columns)
    if (records.filter((record) => record?.category === name).length !== 8)
      errors.push(`分类“${name}”：当前阵列要求八份档案`);
  if (errors.length)
    throw new Error(`档案数据校验失败：\n- ${errors.join("\n- ")}`);
  return content;
}

export async function loadContent() {
  const workbookUrl = new URL(
    "../public/content/site-content.xlsx",
    import.meta.url,
  );
  try {
    return validateContent(await loadWorkbookContent(workbookUrl));
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
    return validateContent(
      JSON.parse(
        await fs.readFile(
          new URL("../content/archives.json", import.meta.url),
          "utf8",
        ),
      ),
    );
  }
}

export function archiveText(r) {
  return `\uFEFFSEE / SHOW · 设计作品档案\nPROJECT ${r.id} / ${r.title}\n${r.en}\n\n分类：${r.category}\n时间：${r.date}\n个人角色：${r.lead}\n工具：${r.tools}\n${r.video ? `视频：${r.video}\n` : ""}状态：概念占位，非真实项目履历\n\n${r.abstract}\n\n设计过程\n${r.findings.join("\n")}\n\n本档案与图像为可替换的作品集示例。\n`;
}
