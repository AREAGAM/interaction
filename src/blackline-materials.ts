import * as THREE from "three";
export function blacklineMaterial(
  material: THREE.MeshPhysicalMaterial,
  name: string,
  array = false,
) {
  material.envMapIntensity = 0.72;
  material.emissive?.set("#000000");
  material.emissiveIntensity = 0;
  const steel = (color: string, roughness: number, metalness = 0.85) => {
    material.color.set(color);
    material.roughness = roughness;
    material.metalness = metalness;
    material.transmission = 0;
  };
  switch (name) {
    case "Particle_Clear_Layer":
      material.color.set(array ? "#18251c" : "#edf6ef");
      material.metalness = 0;
      material.roughness = array ? 0.32 : 0.035;
      material.transmission = array ? 0 : 0.98;
      material.thickness = 0.018;
      material.ior = 1.46;
      material.envMapIntensity = 0.3;
      material.attenuationColor.set("#edf6ef");
      material.attenuationDistance = 8;
      break;
    case "Video_Panel":
      material.color.set("#d8e6dc");
      material.metalness = 0;
      material.roughness = 0.045;
      material.transmission = 0.96;
      material.thickness = 0.012;
      material.envMapIntensity = 0.25;
      break;
    case "Frosted_Polymer":
      // Restore the light edition's dielectric cover: dark albedo tints even
      // fully transmitted light, so a dark glass base obscured the internals.
      material.color.set("#fffdfa");
      material.metalness = 0;
      material.transmission = array ? 0.78 : 0.9;
      material.thickness = 0.12;
      material.roughness = array ? 0.28 : 0.21;
      material.ior = 1.46;
      material.attenuationColor.set("#f2f5f3");
      material.attenuationDistance = 4;
      material.envMapIntensity = 0.6;
      material.clearcoat = array ? 0.3 : 0.1;
      material.clearcoatRoughness = 0.25;
      material.transparent = false;
      material.opacity = 1;
      break;
    case "Ivory_Edges":
      steel(array ? "#78847a" : "#d3ddd5", 0.14, 0.96);
      break;
    case "Titanium_Fasteners":
      steel("#ccd4cf", 0.19, 0.98);
      break;
    case "Internal_Ceramic":
      steel("#68736c", 0.44, 0.3);
      material.envMapIntensity = 1.05;
      material.emissive.set("#b5c3bb");
      material.emissiveIntensity = 0.045;
      break;
    case "Optical_Diffuser":
      steel(array ? "#020503" : "#48554c", 0.44, 0.32);
      material.envMapIntensity = array ? 0.72 : 1.05;
      if (!array) {
        material.emissive.set("#b5c3bb");
        material.emissiveIntensity = 0.025;
      }
      break;
    case "Subsurface_Optics":
      steel("#a4aea8", 0.28, 0.65);
      material.envMapIntensity = 1.25;
      material.emissive.set("#c0cdc5");
      material.emissiveIntensity = 0.035;
      break;
    case "Optical_Edges":
      steel("#c8d1cc", 0.24, 0.75);
      material.envMapIntensity = 1.15;
      break;
    case "Printed_Label":
      steel("#020603", 0.65, 0.08);
      break;
    case "Champagne_Index":
      steel("#b6ff00", 0.22, 0.18);
      material.emissive.set("#99ff00");
      material.emissiveIntensity = array ? 0.22 : 0.4;
      break;
    case "Amber_Lightguide":
      steel("#b6ff00", 0.18, 0.1);
      material.emissive.set("#9dff00");
      material.emissiveIntensity = 0.7;
      break;
    default:
      steel("#26382a", 0.36, 0.68);
  }
}
