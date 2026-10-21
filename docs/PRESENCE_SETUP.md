# JAPULSE 실제 접속자 수: Firebase 웹 콘솔에서 직접 연결하기

ChatGPT의 Firebase 앱 연결은 필요 없습니다. 준비된 웹 프론트엔드에서 Firebase Realtime Database에 직접 연결할 수 있습니다.

## 설정

1. https://console.firebase.google.com/ 접속 → 프로젝트 추가 (예: JAPULSE). Firebase가 아닌 Google 계정 로그인이 필요합니다.
2. 프로젝트 설정(톱니바퀴) → 일반 → 내 앱 → 웹 앱(</>) 등록. 웹 앱 `apiKey`, `authDomain`, `projectId`, `appId` 확인.
3. Build → Authentication → Sign-in method → 익명(Anonymous) 로그인 활성화. 사이트 방문자는 회원가입할 필요 없습니다.
4. Build → Realtime Database → 데이터베이스 만들기. 실제 `databaseURL`을 확인. **공개 읽기·쓰기 테스트 모드 금지**.
5. Realtime Database → 규칙 탭에 GitHub `docs/firebase-presence-rules.json` 내용을 복사하고 **게시**. 다른 경로의 기존 데이터가 이미 있다면 규칙을 통째로 덮어쓰지 말고 병합 후 검증하세요.
6. Authentication → Settings → Authorized domains에 japulse.com이 없으면 추가합니다.
7. GitHub `assets/presence-config.js` 에 있는 null을 아래 본인의 Firebase **웹 앱** 설정으로 교체하고 커밋합니다.

```javascript
export const firebaseConfig = {
  apiKey: "Firebase 웹 API 키",
  authDomain: "your-project.firebaseapp.com",
  databaseURL: "https://your-project-default-rtdb.REGION.firebasedatabase.app",
  projectId: "your-project",
  appId: "Firebase 웹 앱 ID"
};
```

주의: 이 객체는 Firebase **공개 클라이언트 설정**입니다. Firebase 서비스 계정 JSON, 개인 키, 비밀번호, 관리자 인증 토큰을 올리면 안 됩니다.

## 테스트

https://japulse.com/live/ 에서 휴대폰/다른 브라우저로 접속한 뒤 숫자가 실제 사용자 수에 따라 변경되는지 확인합니다. 같은 브라우저 여러 탭은 Firebase 익명 UID 기준 1명으로 셉니다. 다른 기기는 별도 집계될 수 있습니다. 접속 해제 감지는 몇 초 지연될 수 있습니다.

- 연결 전 또는 오류 시: 숫자 숨김(가짜 숫자 표시 안 함).
- `?presence_demo=1`: **DEMO라고 명시된 별도 시뮬레이션**. 일반 접속 시 표시되지 않음.
- 0이나 정확하지 않은 상태면 실시간 집계를 과장하지 않습니다.
- 접속자는 **사이트 접속 중인 브라우저**를 의미하며 실제 영상 재생 중 시청자를 의미하지 않습니다.
- Realtime Database에는 랜덤 Firebase UID별 연결 슬롯의 `true`만 저장합니다. 이메일·이름·IP를 직접 저장하지 않습니다. Firebase 플랫폼 자체가 수집하는 접속/기기 데이터는 제공사 정책을 따릅니다.
- 저장량과 비용을 Firebase 콘솔에서 모니터링하세요. 동시 접속자가 매우 많아지면 전체 접속 UID 목록을 읽는 v1 방식 대신 서버에서 집계하는 방식으로 전환하세요.

원복은 `assets/presence-config.js`를 다시 `null`로 변경하면 됩니다. 기존 JAPULSE LIVE·NOW, 검색 색인은 변경하지 않습니다.

공식 안내: https://firebase.google.com/docs/database/web/offline-capabilities 및 https://firebase.google.com/docs/auth/web/anonymous-auth
