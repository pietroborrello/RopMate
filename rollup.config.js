import npm from "rollup-plugin-node-resolve";

export default {
  input: "js/d3.js",
  plugins: [npm({jsnext: true})],
  output: {
    file: 'build/d3.js',
    format: 'umd',
    name: 'd3',
    sourcemap: true
  }
};
