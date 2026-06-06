const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const root = path.resolve(__dirname, "..");
const dist = path.join(root, "dist");
const tsc = path.join(root, "node_modules", "typescript", "bin", "tsc");
const commands = fs
  .readdirSync(path.join(root, "src", "commands"))
  .filter((name) => name.endsWith(".ts"))
  .sort();

fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(dist, { recursive: true });

for (const command of commands) {
  const output = path.join(dist, command.replace(/\.ts$/, ".jsx"));
  const args = [
    tsc,
    "--target", "ES5",
    "--module", "none",
    "--noLib",
    "--skipLibCheck",
    "--removeComments", "false",
    "--outFile", output,
    path.join(root, "src", "core", "runtime.ts"),
    path.join(root, "src", "editorial", "operations.ts"),
    path.join(root, "src", "commands", command),
  ];
  const result = spawnSync(process.execPath, args, { cwd: root, encoding: "utf8" });
  if (result.status !== 0) {
    process.stderr.write(result.stdout || "");
    process.stderr.write(result.stderr || "");
    process.exit(result.status || 1);
  }
  const source = fs.readFileSync(output, "utf8");
  fs.writeFileSync(
    output,
    "// Brooke Adobe Automation - original ExtendScript-safe JSX\n" + source,
    "utf8",
  );
}

console.log(`Built ${commands.length} standalone JSX commands.`);
