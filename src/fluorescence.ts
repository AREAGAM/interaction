import { Vector2 } from "three";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
// Only HDR highlights bloom: shadows and normal text keep a clean black floor.
export const createFluorescence = () => new UnrealBloomPass(new Vector2(1, 1), .16, .08, 1.5);
