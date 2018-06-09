import npm from "rollup-plugin-node-resolve";

export default {
  entry: "js/d3.js",
  plugins: [npm({jsnext: true})],
  moduleId: "d3",
  moduleName: "d3",
  format: "umd"
};