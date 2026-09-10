import { readSheet } from "read-excel-file/browser";
import fallback from "../content/archives.json" with { type: "json" };

export interface ArchiveRecord {
  id: string;
  title: string;
  en: string;
  department: string;
  category: string;
  date: string;
  lead: string;
  clearance: string;
  abstract: string;
  findings: string[];
  source: string;
  image: string;
  imageAlt: string;
  tools: string;
  placeholder: boolean;
  video?: string;
}
export interface SiteCopy {
  brandFull: string;
  brandShort: string;
  brandChinese: string;
  introLabel: string;
  introTitle: string;
  introSubtitle: string;
  introMeta: string;
  pageDescription: string;
}
export const siteCopy: SiteCopy = {
  brandFull: "SEE / SHOW DESIGN STUDIO",
  brandShort: "SEE / SHOW",
  brandChinese: "夕秀设计工作室",
  introLabel: "INDEPENDENT DESIGNER / 综合设计个人作品集",
  introTitle: "空间，及其可能。",
  introSubtitle: "建筑设计 · VR 技术美术 · AI 视觉探索",
  introMeta: "BLACKLINE / 02 · 48 PROJECT STUDIES",
  pageDescription:
    "夕秀设计工作室，建筑设计与 VR 技术美术的综合设计个人作品集。",
};
export const records: ArchiveRecord[] = structuredClone(fallback.records);
export const archiveColumns: string[] = [...fallback.columns];
export const categories: string[] = ["全部档案", ...fallback.categories];
const workbookUrl = "/content/site-content.xlsx";
let workbookFingerprint = "";
const cellText = (value: unknown) =>
  value == null
    ? ""
    : value instanceof Date
      ? value.toISOString().slice(0, 10)
      : String(value).trim();
function hashBytes(bytes: Uint8Array) {
  let hash = 2166136261;
  for (const byte of bytes) {
    hash ^= byte;
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0).toString(16);
}
async function fetchWorkbook() {
  const response = await fetch(`${workbookUrl}?v=${Date.now()}`, {
    cache: "no-store",
  });
  if (!response.ok)
    throw new Error(`内容表无法读取（HTTP ${response.status}）`);
  const buffer = await response.arrayBuffer();
  return { buffer, fingerprint: hashBytes(new Uint8Array(buffer)) };
}
async function parseWorkbook(buffer: ArrayBuffer) {
  const [settingRows, categoryRows, projectRows] = await Promise.all([
    readSheet(buffer, "网站设置"),
    readSheet(buffer, "分类设置"),
    readSheet(buffer, "项目内容"),
  ]);
  const settingValues = new Map<string, string>();
  for (const row of settingRows.slice(3)) {
    const key = cellText(row[0]);
    if (key) settingValues.set(key, cellText(row[1]));
  }
  const requiredSettings: Record<keyof SiteCopy, string> = {
    brandFull: "brand_full_en",
    brandShort: "brand_short_en",
    brandChinese: "brand_cn",
    introLabel: "intro_label",
    introTitle: "intro_title",
    introSubtitle: "intro_subtitle",
    introMeta: "intro_meta",
    pageDescription: "page_description",
  };
  const nextCopy = { ...siteCopy };
  for (const [property, key] of Object.entries(requiredSettings) as [
    keyof SiteCopy,
    string,
  ][]) {
    const value = settingValues.get(key);
    if (value) nextCopy[property] = value;
  }
  const nextColumns = categoryRows
    .slice(3)
    .map((row) => cellText(row[1]))
    .filter(Boolean);
  if (nextColumns.length !== 6 || new Set(nextColumns).size !== 6)
    throw new Error("分类设置必须保留六个不重复的分类名称");
  const nextRecords: ArchiveRecord[] = projectRows
    .slice(3)
    .filter((row) => cellText(row[0]))
    .map((row) => {
      const get = (index: number) => cellText(row[index]);
      const id = get(0);
      return {
        id,
        category: get(1),
        title: get(2),
        en: get(3),
        department: get(4) || get(1),
        date: get(5),
        lead: get(6),
        clearance: get(7),
        abstract: get(8),
        findings: [get(9), get(10), get(11), get(12)].filter(Boolean),
        tools: get(13),
        image: get(14),
        imageAlt: get(15) || `${get(2)} 项目图片`,
        video: get(16),
        source: get(17) || `/projects/${id}.md`,
        placeholder: true,
      };
    });
  if (nextRecords.length !== 48) throw new Error("项目内容必须保留 48 行项目");
  nextRecords.forEach((record, index) => {
    const expected = `X-${String(index + 1).padStart(3, "0")}`;
    if (record.id !== expected)
      throw new Error(`第 ${index + 1} 个项目编号应为 ${expected}`);
    const required = [
      record.category,
      record.title,
      record.en,
      record.date,
      record.lead,
      record.clearance,
      record.abstract,
      record.tools,
      record.image,
    ];
    if (required.some((value) => !value))
      throw new Error(`${record.id} 存在必填内容为空`);
    if (!nextColumns.includes(record.category))
      throw new Error(`${record.id} 使用了未定义分类“${record.category}”`);
  });
  for (const category of nextColumns)
    if (
      nextRecords.filter((record) => record.category === category).length !== 8
    )
      throw new Error(`分类“${category}”必须包含八个项目`);
  return { nextCopy, nextColumns, nextRecords };
}
export async function loadEditableContent() {
  try {
    const { buffer, fingerprint } = await fetchWorkbook();
    workbookFingerprint = fingerprint;
    const { nextCopy, nextColumns, nextRecords } = await parseWorkbook(buffer);
    Object.assign(siteCopy, nextCopy);
    records.splice(0, records.length, ...nextRecords);
    archiveColumns.splice(0, archiveColumns.length, ...nextColumns);
    categories.splice(0, categories.length, "全部档案", ...nextColumns);
    document.title = `${siteCopy.brandFull} · ${siteCopy.brandChinese}`;
    document
      .querySelector('meta[name="description"]')
      ?.setAttribute("content", siteCopy.pageDescription);
    return { source: "workbook" as const };
  } catch (error) {
    const message = error instanceof Error ? error.message : "内容表读取失败";
    console.warn("Using bundled content fallback:", error);
    return { source: "fallback" as const, error: message };
  }
}
export function watchEditableContent() {
  if (!["127.0.0.1", "localhost"].includes(location.hostname)) return;
  window.setInterval(async () => {
    try {
      const next = await fetchWorkbook();
      if (!workbookFingerprint || next.fingerprint !== workbookFingerprint)
        location.reload();
    } catch {}
  }, 2000);
}
export function columnFiles(lane: number) {
  return records
    .map((record, index) => ({ record, index }))
    .filter(({ record }) => record.category === archiveColumns[lane])
    .map(({ index }) => index);
}
export function fileLocation(index: number) {
  const lane = archiveColumns.indexOf(records[index].category);
  const row = 12 + columnFiles(lane).indexOf(index);
  return { lane, row, slot: lane * 32 + row };
}
export function fileAtSlot(slot: number) {
  const files = columnFiles(Math.floor(slot / 32));
  return files[Math.max(0, Math.min(files.length - 1, (slot % 32) - 12))];
}
