<fieldset>
    <div class="form-group">
        <label for="f_name">Question *</label>
          <input type="text" name="f_name" placeholder="Question" class="form-control" required="required" id = "f_name" value="<?php echo htmlspecialchars($edit ? $customer['f_name'] : '', ENT_QUOTES, 'UTF-8'); ?>" >
    </div> 

    <div class="form-group">
        <label for="l_name">Answer *</label>
        <input type="text" name="l_name" placeholder="Answer" class="form-control" required="required" id="l_name" value="<?php echo htmlspecialchars($edit ? $customer['l_name'] : '', ENT_QUOTES, 'UTF-8'); ?>">
    </div> 

    <div class="form-group text-center">
        <label></label>
        <button type="submit" class="btn btn-warning" >Save <span class="glyphicon glyphicon-send"></span></button>
    </div>            
</fieldset>