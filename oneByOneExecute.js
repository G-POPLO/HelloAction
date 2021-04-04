const exec = require("child_process").execSync;
const fs = require("fs");
const download = require("download");
const smartReplace = require("./smartReplace");

// 公共变量
const JD_COOKIE = process.env.JD_COOKIE; //cokie,多个用&隔开即可
const SyncUrl = process.env.SYNCURL; //签到地址,方便随时变动
let CookieJDs = [];

async function downFile() {
    await download(SyncUrl, "./", { filename: "temp.js" });
}

async function changeFiele(content, cookie) {
    let newContent = await smartReplace.replaceWithSecrets(content, cookie);
    await fs.writeFileSync("./execute.js", newContent, "utf8");
}

async function executeOneByOne() {
    const content = await fs.readFileSync("./temp.js", "utf8");
    for (var i = 0; i < CookieJDs.length; i++) {
        console.log(`正在执行第${i + 1}个账号签到任务`);
        await changeFiele(content, CookieJDs[i]);
        console.log("替换变量完毕");
        try {
            await exec("node execute.js", { stdio: "inherit" });
        } catch (e) {
            console.log("执行异常:" + e);
        }
        console.log("执行完毕");
    }
}

async function start() {
    console.log(`当前执行时间:${new Date().toString()}`);
    if (!JD_COOKIE) {
        console.log("请填写 JD_COOKIE 后在继续");
        return;
    }
    if (!SyncUrl) {
        console.log("请填写 SYNCURL 后在继续");
        return;
    }
    CookieJDs = JD_COOKIE.split("&");
    console.log(`当前共${CookieJDs.length}个账号需要签到`);
    // 下载最新代码
    await downFile();
    console.log("下载代码完毕");
    await executeOneByOne();
    console.log("全部执行完毕");
}

start();
