import numpy as np

def fuse_tracks(cam_tracks, reid_embeddings, distance_thresh=0.5):
    # cam_tracks: dict of {cam_id: {track_id: (x, y)}}
    # reid_embeddings: dict of {cam_id: {track_id: embedding}}
    # Returns: fused_tracks: {global_id: (x, y)}
    # Placeholder: naive fusion by spatial proximity and embedding distance
    fused_tracks = {}
    global_id = 0
    used = set()
    for cam1, tracks1 in cam_tracks.items():
        for tid1, pos1 in tracks1.items():
            emb1 = reid_embeddings[cam1][tid1]
            matched = False
            for cam2, tracks2 in cam_tracks.items():
                if cam1 == cam2:
                    continue
                for tid2, pos2 in tracks2.items():
                    emb2 = reid_embeddings[cam2][tid2]
                    dist = np.linalg.norm(emb1 - emb2)
                    if dist < distance_thresh:
                        fused_tracks[global_id] = ((np.array(pos1) + np.array(pos2)) / 2).tolist()
                        used.add((cam1, tid1))
                        used.add((cam2, tid2))
                        global_id += 1
                        matched = True
                        break
                if matched:
                    break
            if not matched and (cam1, tid1) not in used:
                fused_tracks[global_id] = pos1
                global_id += 1
    return fused_tracks 