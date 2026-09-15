import * as THREE from "three";
export type ParticleSeeds = number[][];
let seedPromise: Promise<ParticleSeeds> | undefined;
export function loadParticleSeeds() {
  return (seedPromise ??= fetch("/assets/particles/particle-seeds.json")
    .then((r) => {
      if (!r.ok) throw new Error("Particle seeds unavailable");
      return r.json();
    })
    .then((data) => data.particles)
    .catch((error) => {
      seedPromise = undefined;
      throw error;
    }));
}
export function createParticleCloud(seeds: ParticleSeeds) {
  const n = seeds.length,
    positions = new Float32Array(n * 3),
    parameters = new Float32Array(n * 2),
    colors = new Float32Array(n * 3);
  seeds.forEach(([x, y, z, phase, size, tint], i) => {
    positions.set([x, z, -y], i * 3);
    parameters.set([phase, size], i * 2);
    colors.set(tint ? [0.6, 1, 0.055] : [0.72, 0.9, 0.8], i * 3);
  });
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute(
    "particleParams",
    new THREE.BufferAttribute(parameters, 2),
  );
  geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  geometry.boundingSphere = new THREE.Sphere(
    new THREE.Vector3(0, 1.74, 0.06),
    2.4,
  );
  const material = new THREE.ShaderMaterial({
    vertexColors: true,
    transparent: false,
    depthWrite: true,
    toneMapped: false,
    fog: true,
    uniforms: {
      ...THREE.UniformsUtils.clone(THREE.UniformsLib.fog),
      uTime: { value: 0 },
      uHeight: { value: 1080 },
      uSpread: { value: 0 },
      uBrightness: { value: 1 },
    },
    vertexShader: `attribute vec2 particleParams;uniform float uTime;uniform float uHeight;uniform float uSpread;varying vec3 vColor;
      #include <fog_pars_vertex>
      void main(){float t=uTime*1.57079632679;vec3 p=position;p.z*=1.+10.*uSpread;
        p.x+=.035*sin(t+particleParams.x)+.02*cos(2.*t+position.y*2.);
        p.y+=.027*cos(t+particleParams.x)+.015*sin(2.*t+position.x*2.);
        p.z-=.005*sin(2.*t+particleParams.x+position.x);
        vec4 mvPosition=modelViewMatrix*vec4(p,1.);gl_Position=projectionMatrix*mvPosition;
        gl_PointSize=clamp(particleParams.y*uHeight*projectionMatrix[1][1]/max(.1,-mvPosition.z),.7,4.5);
        vColor=color*(.82+.18*sin(t+particleParams.x));
        #include <fog_vertex>
      }`,
    fragmentShader: `uniform float uBrightness;varying vec3 vColor;
      #include <fog_pars_fragment>
      void main(){float r=length(gl_PointCoord-.5);if(r>.47)discard;float light=1.-smoothstep(.1,.5,r);gl_FragColor=vec4(vColor*light*uBrightness,1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
        #include <fog_fragment>
      }`,
  });
  const cloud = new THREE.Points(geometry, material);
  cloud.name = "Archive_GPU_Particles";
  cloud.userData.particleCloud = true;
  cloud.userData.assemblyPart = "optical-core";
  cloud.raycast = () => {};
  return cloud;
}
export function updateParticleClouds(
  root: THREE.Object3D,
  time: number,
  height: number,
  spread = 0,
  quality = 1,
  brightness = 1,
) {
  root.traverse((o) => {
    if (!o.userData.particleCloud) return;
    const cloud = o as THREE.Points<THREE.BufferGeometry, THREE.ShaderMaterial>;
    cloud.material.uniforms.uTime.value = time;
    cloud.material.uniforms.uHeight.value = height;
    cloud.material.uniforms.uSpread.value = spread;
    cloud.material.uniforms.uBrightness.value = brightness;
    cloud.geometry.setDrawRange(
      0,
      Math.round(
        96 +
          (cloud.geometry.attributes.position.count - 96) *
            THREE.MathUtils.clamp(quality, 0, 1),
      ),
    );
  });
}
// Background archives share one small geometry and one draw call. No particle-proxy meshes.
export function createArrayParticles(seeds: ParticleSeeds, count: number) {
  const positions: number[] = [],
    colors: number[] = [],
    indices: number[] = [];
  seeds.slice(0, 96).forEach(([x, y, z, _phase, size, tint], i) => {
    const r = size * 0.9;
    positions.push(
      x - r,
      z - r,
      -y,
      x + r,
      z - r,
      -y,
      x + r,
      z + r,
      -y,
      x - r,
      z + r,
      -y,
    );
    for (let j = 0; j < 4; j++)
      colors.push(...(tint ? [0.4, 0.65, 0.015] : [0.25, 0.34, 0.28]));
    const k = i * 4;
    indices.push(k, k + 1, k + 2, k, k + 2, k + 3);
  });
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
  g.setIndex(indices);
  const m = new THREE.MeshBasicMaterial({
    vertexColors: true,
    side: THREE.DoubleSide,
    toneMapped: false,
  });
  const mesh = new THREE.InstancedMesh(g, m, count);
  mesh.name = "Archive_Array_Particles_96";
  mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  mesh.frustumCulled = false;
  mesh.raycast = () => {};
  return mesh;
}
