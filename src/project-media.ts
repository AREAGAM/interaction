import * as THREE from "three";
import type { ArchiveRecord } from "./data";
const selectedVideos = new Map<string, { url: string; name: string }>();
addEventListener("beforeunload", () => {
  for (const item of selectedVideos.values()) URL.revokeObjectURL(item.url);
});
export async function createProjectMedia(
  surface: THREE.Mesh,
  record: ArchiveRecord,
) {
  let disposed = false,
    video: HTMLVideoElement | undefined,
    videoTexture: THREE.VideoTexture | undefined,
    error = "",
    name = "",
    request = 0;
  const poster = await new THREE.TextureLoader().loadAsync(record.image);
  poster.colorSpace = THREE.SRGBColorSpace;
  poster.flipY = false;
  const original = surface.material;
  const material = new THREE.MeshBasicMaterial({
    map: poster,
    toneMapped: false,
    side: THREE.DoubleSide,
  });
  surface.material = material;
  const releaseVideo = () => {
    if (video) {
      video.pause();
      video.removeAttribute("src");
      video.load();
      video = undefined;
    }
    videoTexture?.dispose();
    videoTexture = undefined;
  };
  const bind = (url: string, label: string) => {
    releaseVideo();
    error = "";
    name = label;
    video = document.createElement("video");
    video.src = url;
    video.preload = "metadata";
    video.loop = true;
    video.muted = true;
    video.playsInline = true;
    video.addEventListener("error", () => {
      error = "该视频无法播放，请选择其他文件";
      material.map = poster;
      material.needsUpdate = true;
    });
  };
  const remembered = selectedVideos.get(record.id);
  if (remembered) bind(remembered.url, remembered.name);
  else if (record.video) bind(record.video, "项目视频");
  const play = async () => {
    const target = video,
      ticket = ++request;
    if (!target || disposed) return;
    try {
      await target.play();
      if (disposed || ticket !== request || target !== video) {
        target.pause();
        return;
      }
      if (!videoTexture) {
        videoTexture = new THREE.VideoTexture(target);
        videoTexture.colorSpace = THREE.SRGBColorSpace;
        videoTexture.flipY = false;
      }
      material.map = videoTexture;
      material.needsUpdate = true;
      error = "";
    } catch {
      if (!disposed) error = "视频未能播放，请重试或更换文件";
    }
  };
  return {
    async setFile(file: File) {
      if (disposed) return;
      if (
        !file.type.startsWith("video/") &&
        !/\.(mp4|webm|mov|m4v)$/i.test(file.name)
      )
        throw new Error("请选择视频文件");
      request++;
      const old = selectedVideos.get(record.id);
      releaseVideo();
      if (old) URL.revokeObjectURL(old.url);
      const next = { url: URL.createObjectURL(file), name: file.name };
      selectedVideos.set(record.id, next);
      bind(next.url, next.name);
      await play();
    },
    async toggle() {
      if (!video) return;
      if (video.paused) await play();
      else video.pause();
    },
    state() {
      return {
        available: !!video,
        playing: !!video && !video.paused,
        name,
        error,
        hasFrame: !!videoTexture,
      };
    },
    dispose() {
      disposed = true;
      request++;
      releaseVideo();
      poster.dispose();
      material.dispose();
      surface.material = original;
    },
  };
}
