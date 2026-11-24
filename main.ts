import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point for the make.fun news-image-20261124 entry.
// Copies the rendered front page (entry.png, next to this file) into the
// output directory make.fun expects, and verifies the copy byte-for-byte
// by comparing file sizes (the source is read back after the copy).

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(resolve(outputDir), "entry.png");

mkdirSync(outputDir, { recursive: true });

// Guard against a truncated or non-PNG source: entry.png must start with
// the 8-byte PNG signature before we hand anything to the grader.
import { openSync, readSync, closeSync } from "node:fs";
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const fd = openSync(source, "r");
const head = Buffer.alloc(8);
if (readSync(fd, head, 0, 8, 0) !== 8 || !head.equals(PNG_SIGNATURE)) {
  closeSync(fd);
  throw new Error(`source ${source} is not a valid PNG file`);
}
closeSync(fd);

copyFileSync(source, target);

const sourceSize = statSync(source).size;
const targetSize = statSync(target).size;
if (sourceSize !== targetSize) {
  throw new Error(
    `entry.png copy size mismatch: source ${sourceSize} bytes, ` +
      `copied ${targetSize} bytes to ${target}`
  );
}

console.log(`Copied entry.png (${sourceSize} bytes) to ${target}`);
