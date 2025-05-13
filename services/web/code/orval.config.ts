import { defineConfig } from 'orval';

export default defineConfig({
  kaleoCore: {
    input: '../../../apis/dist/kaleo-core.yml',
    output: {
      mode: 'tags-split',
      target: './src/api-client',
      schemas: './src/api-client/schemas',
      client: 'react-query',
    },
  },
});
