import { readSheet } from "read-excel-file/node";
const text = (value) =>
  value == null
    ? ""
    : value instanceof Date
      ? value.toISOString().slice(0, 10)
      : String(value).trim();
export async function loadWorkbookContent(path) {
  const [categoryRows, projectRows] = await Promise.all([
    readSheet(path, "分类设置"),
    readSheet(path, "项目内容"),
  ]);
  const columns = categoryRows
    .slice(3)
    .map((row) => text(row[1]))
    .filter(Boolean);
  const records = projectRows
    .slice(3)
    .filter((row) => text(row[0]))
    .map((row) => {
      const get = (index) => text(row[index]);
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
  return { categories: [...columns], columns: [...columns], records };
}
