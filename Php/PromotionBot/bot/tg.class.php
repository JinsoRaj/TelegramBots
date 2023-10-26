<?php
class TG {
  
    public $token = '';
  
    public function __construct($token) {
        $this->token = $token; 
    }
      
    public function send($id, $message, $kb) {
        $data = array(
            'chat_id' => $id,
            'text'  => $message,
            'parse_mode' => 'HTML',
            'disable_web_page_preview'=>true,
            'reply_markup' => json_encode(array('inline_keyboard' => $kb))
        );
        $this->request('sendMessage', $data);
    }  

    public function editMessageText($id, $m_id, $m_text, $kb=''){
        $data=array(
             'chat_id' => $id,
             'message_id' => $m_id,
             'parse_mode' => 'HTML',
             'text' => $m_text
        );
        if($kb)
            $data['reply_markup']=json_encode(array('inline_keyboard' => $kb));

        $this->request('editMessageText', $data); 
    }


    public function editMessageReplyMarkup($id, $m_id, $kb){
        $data=array(
             'chat_id' => $id,
             'message_id' => $m_id,
            'reply_markup' => json_encode(array('inline_keyboard' => $kb))
        );
        $this->request('editMessageReplyMarkup', $data); 
    }
    
    public function answerCallbackQuery($cb_id, $message) {
        $data = array(
            'callback_query_id'      => $cb_id,
            'text'     => $message
        );
        $this->request('answerCallbackQuery', $data);
    } 

    public function sendChatAction($id,$action='typing') {
        $data = array(
            'chat_id' => $id,
            'action'     => $action
        );
        $this->request('sendChatAction', $data);
    }


    public  function request($method, $data = array()) {
        $curl = curl_init();
          
        curl_setopt($curl, CURLOPT_URL, 'https://api.telegram.org/bot' . $this->token .  '/' . $method);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'POST'); 
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
          
        $out = json_decode(curl_exec($curl), true);
          
        curl_close($curl);
        return $out;
    }
}
?>