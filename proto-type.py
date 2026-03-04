timetable = ["バンドA", "バンドB", "バンドC"]

# スキル: 5(卓メイン可), 3(ステージメイン可), 1(初心者)
# count: これまでにシフトに入った回数（優先度計算に使う）
members = [
    {"name": "ベテラン先輩", "skill": 5, "count": 0, "ng": ["バンドA"], "req": ["バンドC"]},
    {"name": "自分", "skill": 5, "count": 0, "ng": ["バンドC"], "req": []},
    {"name": "中堅同期", "skill": 3, "count": 0, "ng": [], "req": ["バンドA"]},
    {"name": "初心者後輩1", "skill": 1, "count": 0, "ng": [], "req": []},
    {"name": "初心者後輩2", "skill": 1, "count": 0, "ng": ["バンドB"], "req": []},
    {"name": "初心者後輩3", "skill": 1, "count": 0, "ng": [], "req": []}
]

shift_result = {}

for band in timetable:
    desk_team = []
    stage_team = []
    desk_score = 0
    stage_score = 0

    # 1. NGの人を除外して、この枠に入れる候補者リストを作成
    available = []
    for m in members:
        if band not in m["ng"]:
            # 優先度ポイントの計算
            # 基本は「シフトに入った回数が少ない人」を優先（回数が多いとマイナス）
            priority = -m["count"] * 10 
            
            # 希望(req)を出している枠ならボーナスポイント
            if band in m["req"]:
                priority += 100
                
            # 同じ優先度ならスキルが高い人を先に選ぶための微調整
            priority += m["skill"]
            
            # 候補者のデータに優先度を一時的に持たせてリストに追加
            candidate = m.copy()
            candidate["priority"] = priority
            available.append(candidate)
    
    # 2. 優先度ポイントが高い順に並び替え（ここがアルゴリズムの肝）
    available.sort(key=lambda x: x["priority"], reverse=True)

    # 3. 卓チームを組む（目標：スキル合計5以上）
    remaining = []
    for m in available:
        if desk_score < 5:
            desk_team.append(m)
            desk_score += m["skill"]
        else:
            # 卓チームから漏れた人はステージチームの候補に回す
            remaining.append(m)
            
    # 4. ステージチームを組む（目標：スキル合計3以上）
    for m in remaining:
        if stage_score < 3:
            stage_team.append(m)
            stage_score += m["skill"]
    
    # 5. 結果の保存と、選ばれた人の「シフト入った回数(count)」を増やす
    if desk_score >= 5 and stage_score >= 3:
        shift_result[band] = {
            "卓": [m["name"] for m in desk_team], 
            "ステージ": [m["name"] for m in stage_team]
        }
        # 元のmembersリストのcountを更新
        assigned_names = [m["name"] for m in desk_team + stage_team]
        for m in members:
            if m["name"] in assigned_names:
                m["count"] += 1
    else:
        shift_result[band] = {"エラー": "スキル条件を満たすメンバーが足りません！要手動調整"}

# 結果を出力して確認
print("--- シフト作成結果 ---")
for band, teams in shift_result.items():
    print(f"【{band}】: {teams}")
    
print("\n--- 最終的なシフト入数 ---")
for m in members:
    print(f"{m['name']}: {m['count']}回")