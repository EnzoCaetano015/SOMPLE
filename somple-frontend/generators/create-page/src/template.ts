import { createTemplate } from "bingo";
import { z } from "zod";

export default createTemplate({
  options: {
    name: z
      .string()
      .min(1)
      .describe("Nome da página (ex: Dashboard, Equipment, Audit)"),
  },

  produce({ options }) {
    const { name } = options;

    return {
      files: {
        [`${name}.tsx`]: `export const ${name} = () => {
  return <div>${name}</div>;
};
`,

        [`${name}.hook.ts`]: `export const use${name} = () => {
  return {};
};
`,

        [`${name}.types.ts`]: `export interface ${name}Props {}
`,

        [`${name}.utils.ts`]: `// Utilitários para ${name}
`,
      },
    };
  },
});